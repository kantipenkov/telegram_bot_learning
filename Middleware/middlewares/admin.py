from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config import Config


class GreetAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        config: Config = data["config"]
        user: User = data["event_from_user"]
        data["admin"] = user.id in config.bot.admins
        return await handler(event, data)
