import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from commands import Commands
from config import config
from handlers import (
    buttons_example,
    command_start,
    general,
    personal_data,
    polls,
    shared_users,
)


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Go to the start page"),
        BotCommand(command=Commands.BUTTONS_EXAMPLE, description="See buttons example"),
        BotCommand(command=Commands.POLL_EXAMPLE, description="Go to POll example"),
        BotCommand(
            command=Commands.PERSONAL_DATA,
            description="Go to work with personal data example",
        ),
        BotCommand(
            command=Commands.SHARED_USERS,
            description="Go to work with shared users/chats example",
        ),
    ]
    await bot.set_my_commands(main_menu_commands)


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
    dp.include_router(command_start.router)
    dp.include_router(buttons_example.router)
    dp.include_router(polls.router)
    dp.include_router(personal_data.router)
    dp.include_router(shared_users.router)
    dp.include_router(general.router)

    dp.startup.register(set_main_menu)
    dp.shutdown.register(delete_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main())
