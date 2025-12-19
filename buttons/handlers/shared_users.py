import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from commands import Commands
from keyboards.shared_users import keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=Commands.SHARED_USERS))
async def shared_users_example(message: Message):
    await message.answer(text="select what to chare", reply_markup=keyboard)


# catch shared user
@router.message(F.user_shared)
async def user_shared(message: Message):
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(F.users_shared)
async def users_shared(message: Message):
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))


@router.message(F.chat_shared)
async def chat_shared(message: Message):
    logger.debug(message.model_dump_json(indent=4, exclude_none=True))
