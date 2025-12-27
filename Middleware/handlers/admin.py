import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import Config
from filters import IsAdmin

logger = logging.getLogger(__name__)

router = Router()


@router.message(IsAdmin(), Command(commands=["admin"]))
async def get_admins(message: Message, config: Config, admin: bool):
    msg = "List of admins: %s" % ("".join(map(str, config.bot.admins)))
    if admin:
        msg += "\n.By the way, hello admin!!"
    await message.answer(msg)
