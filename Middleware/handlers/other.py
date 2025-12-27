import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message, admin: bool):
    msg = "This is a simple echo bot to show usage of middlewares. Type something and look logs"
    if admin:
        msg += "\n.By the way, hello admin!"
    await message.answer(msg)
