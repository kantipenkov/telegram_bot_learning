import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.keyboards import keyboard

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="This is an example that shows message formatting. There are available HTML and Markdown styles. Choose one:",
        reply_markup=keyboard,
    )
