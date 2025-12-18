from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def process_start_command(message: Message):
    await message.reply(text=f"unknown command {message.text}")
