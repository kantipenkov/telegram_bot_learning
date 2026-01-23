import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        db_pool: AsyncConnectionPool | None = data.get("db_pool", None)
        if db_pool is None:
            logger.error("Can't get db pool in middleware data")
            raise RuntimeError("Missing db pool in meddleware context.")
        async with db_pool.connection() as conn:
            try:
                async with conn.transaction():
                    if isinstance(event, Update):
                        data["conn"] = conn
                        result = await handler(event, data)
                    else:
                        raise RuntimeError(
                            "Got inapropriate event type '%s' in middleware data, expected type 'Update'",
                            type(event).__name__,
                        )
            except Exception as e:
                logger.exception("Transaction rolled back due to the error: %s", e)
                raise
        return result
