import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
from handlers import buttons_example, command_start, general, personal_data, polls


async def main() -> None:
    log_level_mapping = logging.getLevelNamesMapping()
    try:
        log_level = log_level_mapping[config.log.level]
    except KeyError:
        log_level = log_level_mapping["DEBUG"]
    logging.basicConfig(level=log_level, format=config.log.format)
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()
    dp.include_router(command_start.router)
    dp.include_router(buttons_example.router)
    dp.include_router(polls.router)
    dp.include_router(personal_data.router)
    dp.include_router(general.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
