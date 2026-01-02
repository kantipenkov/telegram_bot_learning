import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import config
from handlers import other, user


async def delete_commands(bot: Bot):
    await bot.delete_my_commands(BotCommandScopeDefault())


async def main() -> None:
    log_level_mapping = logging.getLevelNamesMapping()
    try:
        log_level = log_level_mapping[config.log.level]
    except KeyError:
        log_level = log_level_mapping["DEBUG"]
    logging.basicConfig(level=log_level, format=config.log.format)
    bot = Bot(token=config.bot.token)
    # you can set up bot with parse mode but in this example we want to use both so we'll put parsing mode in handlers
    # bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    # bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(other.router, user.router)
    await dp.start_polling(bot, config=config)


if __name__ == "__main__":
    asyncio.run(main())
