from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsAdmin
from config import config

router = Router()

@router.message(IsAdmin(config.bot.admins), Command(commands='start'))
async def process_start_admin(message: Message):
    await message.answer('Admin?')
