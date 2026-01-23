import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Update, User

logger = logging.getLogger(__name__)


class LangSettingsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user", None)
        if user is None:
            return await handler(event, data)

        if isinstance(event, Update):
            if event.callback_query is None:
                return await handler(event, data)

            locales: list[str] | None = data.get("locales", None)
            if locales is None:
                logger.warning("Can't get locales, fallback to 'en' locale")
                locales = [
                    "en",
                ]

            state: FSMContext | None = data.get("state", None)
            user_context_data: dict = await state.get_data()

            if event.callback_query.data == "cancel_lang_button_data":
                user_context_data.update(user_lang=None)
                await state.set_data(user_context_data)

            elif (
                event.callback_query.data in locales
                and event.callback_query.data != user_context_data.get("user_lang")
            ):
                user_context_data.update(user_lang=event.callback_query.data)
                await state.set_data(user_context_data)

        return await handler(event, data)
