import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import config
from handlers import admin, other, user
from middlewares import GreetAdmin, LogMiddleware, ReactionMiddleware


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
    dp = Dispatcher()
    dp.include_routers(admin.router, other.router, user.router)
    # register middlewares
    dp.update.middleware(LogMiddleware())
    dp.message.middleware(GreetAdmin())
    # you can also set middlewares for separate routers
    user.router.message.middleware(ReactionMiddleware())
    await dp.start_polling(bot, config=config)


if __name__ == "__main__":
    asyncio.run(main())
