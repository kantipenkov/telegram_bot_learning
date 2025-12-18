import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from commands import Commands
from keyboards.personal_data import keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=Commands.PERSONAL_DATA))
async def personal_data_example(message: Message):
    await message.answer(text="personal_data", reply_markup=keyboard)


@router.message(F.contact)
async def process_contact(message: Message):
    await message.answer(text=f"Your telephone number: {message.contact.phone_number}")
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(F.Location)
async def process_location(message: Message):
    await message.answer(
        text=f"Your location is: {message.location.latitude, message.location.longitude}"
    )
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(Command(commands=Commands.USER_ID))
async def get_user_id(message: Message):
    await message.answer(text=f"Your telegram user id is: {message.from_user.id}")
