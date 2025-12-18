from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from commands import BUTTONS_EXAMPLE
from keyboards.buttons_example import keyboard

router = Router()


@router.message(Command(commands=BUTTONS_EXAMPLE))
async def buttons_answer(message: Message):
    await message.answer(text="What cats are more afraid of?", reply_markup=keyboard)


@router.message(F.text == "Cucumbers")
async def cucumbers_answer(message: Message):
    await message.answer(
        text="Yes, sometimes cats are afraid of cucumbers a lot.",
        # reply_markup=ReplyKeyboardRemove(), # remove keyboard completely
    )


@router.message(F.text == "Dogs")
async def dogs_answer(message: Message):
    await message.answer(
        text="Yes, cats are afraid of dogs but have you ever seen how they are afraid of cucumbers.",
        # reply_markup=ReplyKeyboardRemove(),
    )
