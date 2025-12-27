from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import Config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, config: Config):
        return message.from_user.id in config.bot.admins
