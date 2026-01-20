import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot.handlers import others
from config.config import Config, load_settings


async def main():
    config: Config = load_settings()
    log_level_mapping = logging.getLevelNamesMapping()
    try:
        log_level = log_level_mapping[config.log.level]
    except KeyError:
        log_level = log_level_mapping["DEBUG"]
    logging.basicConfig(level=log_level, format=config.log.format)
    bot = Bot(config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis = Redis(
        host="redis",
        password=config.redis.password,
    )
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    dp.include_routers(others.router)
    await dp.start_polling(bot, config=config)


if __name__ == "__main__":
    asyncio.run(main())
