from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.command_start import keyboard

router = Router()


@router.message(CommandStart())
@router.message(F.text == "Home")
@router.callback_query(F.data == "go_home")
async def process_start_command(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer(text="Choose the demo", reply_markup=keyboard)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text="Choose the demo", reply_markup=keyboard)
        await message.answer()
    else:
        raise TypeError(f"Unknown type of data {type(message)}")
