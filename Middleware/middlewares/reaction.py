import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, ReactionTypeEmoji, TelegramObject

logger = logging.getLogger(__name__)


class ReactionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        if isinstance(event, Message) and event.message_id:
            try:
                await bot.set_message_reaction(
                    chat_id=event.chat.id,
                    message_id=event.message_id,
                    reaction=[ReactionTypeEmoji(emoji="❤")],
                )
            except Exception as e:
                logger.exception("Failed to set reaction")
        result = await handler(event, data)
        # event.effect_id = "5046509860389126442"
        return result
