from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.command_start import keyboard
from lexicon import lexicon

router = Router()


@router.message(CommandStart())
@router.message(F.text == "Home")
@router.callback_query(F.data == "Home")
async def process_start_command(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer(text=lexicon.home_banner, reply_markup=keyboard)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text=lexicon.home_banner, reply_markup=keyboard)
        await message.answer()
    else:
        raise TypeError(f"Unknown type of data {type(message)}")
