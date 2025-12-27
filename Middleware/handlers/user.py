import logging

from aiogram import Bot, F, Router
from aiogram.types import Message, ReactionTypeEmoji

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text)
async def echo(message: Message, bot: Bot):
    if message.text:
        await message.answer(message.text)
