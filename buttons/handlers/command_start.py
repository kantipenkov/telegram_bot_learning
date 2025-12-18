from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.command_start import keyboard

router = Router()


@router.message(CommandStart())
@router.message( F.text == "Home")
async def process_start_command(message: Message):
    await message.answer(text="Choose the demo", reply_markup=keyboard)
