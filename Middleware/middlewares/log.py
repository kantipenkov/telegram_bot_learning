import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)


class LogMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        logger.debug(
            "In %s, event type: %s", self.__class__.__name__, event.__class__.__name__
        )
        result = await handler(event, data)
        logger.debug("Exit %s, result: %s", self.__class__.__name__, result)
        return result
