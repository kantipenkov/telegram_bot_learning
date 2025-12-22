import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.personal_data import keyboard
from lexicon import Commands, lexicon

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=Commands.PERSONAL_DATA))
async def personal_data_example(message: Message):
    await message.answer(text=lexicon.personal_data_banner, reply_markup=keyboard)


@router.message(F.contact)
async def process_contact(message: Message):
    await message.answer(text=f"{lexicon.personal_phone}{message.contact.phone_number}")
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(F.location)
async def process_location(message: Message):
    await message.answer(
        text=f"{lexicon.personal_location}{message.location.latitude, message.location.longitude}"
    )
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(Command(commands=Commands.USER_ID))
async def get_user_id(message: Message):
    await message.answer(text=f"{lexicon.tg_user_id}{message.from_user.id}")
