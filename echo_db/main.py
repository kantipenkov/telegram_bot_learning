import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot import main
from app.bot.handlers import others
from config import config

log_level_mapping = logging.getLevelNamesMapping()
try:
    log_level = log_level_mapping[config.log.level]
except KeyError:
    log_level = log_level_mapping["DEBUG"]
logging.basicConfig(level=log_level, format=config.log.format)


if __name__ == "__main__":
    asyncio.run(main(config))
