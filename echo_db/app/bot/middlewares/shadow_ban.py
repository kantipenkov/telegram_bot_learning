import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_banned_status_by_user_id

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user", None)

        if user is None:
            return await handler(event, data)

        conn: AsyncConnection | None = data.get("conn", None)
        if conn is None:
            logger.error("Database connection not found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")

        user_banned_status = await get_user_banned_status_by_user_id(
            conn, user_id=user.id
        )

        if user_banned_status:
            logger.warning("Shadow-banned user tried to interact: %d", user.id)
            if isinstance(event, Update):
                if event.callback_query:
                    await event.callback_query.answer()
            else:
                raise RuntimeError(
                    "Got inapropriate event type '%s' in middleware data, expected type 'Update'",
                    type(event).__name__,
                )
            return

        return await handler(event, data)
