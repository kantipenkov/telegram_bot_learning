import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_lang

logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user", None)

        if user is None:
            return await handler(event, data)

        state: FSMContext | None = data.get("state", None)
        user_context_data = await state.get_data()

        if (user_lang := user_context_data.get("user_lang")) is None:

            conn: AsyncConnection | None = data.get("conn", None)
            if conn is None:
                logger.error("Database connection not found in middleware data.")
                raise RuntimeError(
                    "Missing database connection for detecting the user's language."
                )

            user_lang: str | None = await get_user_lang(conn, user_id=user.id)
            if user_lang is None:
                user_lang = user.language_code

        translations: dict | None = data.get("translations", None)
        i18n: dict | None = translations.get(user_lang, None)

        if i18n is None:
            data["i18n"] = translations[translations["default"]]
        else:
            data["i18n"] = i18n

        return await handler(event, data)
