from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.buttons_example import keyboard
from lexicon import Commands, lexicon

router = Router()


@router.message(Command(commands=Commands.BUTTONS_EXAMPLE))
async def buttons_answer(message: Message):
    await message.answer(text=lexicon.cat_question, reply_markup=keyboard)


@router.message(F.text == lexicon.cat_cucumber)
async def cucumbers_answer(message: Message):
    await message.answer(
        text=lexicon.cat_cucumber_answer,
        # reply_markup=ReplyKeyboardRemove(), # remove keyboard completely
    )


@router.message(F.text == lexicon.cat_dog)
async def dogs_answer(message: Message):
    await message.answer(
        text=lexicon.cat_dog_answer,
        # reply_markup=ReplyKeyboardRemove(),
    )
