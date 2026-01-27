import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from config import load_settings
from handlers import lang, others, user
from middlewares.i18n_middleware import UserManager


async def main() -> None:
    config = load_settings()
    log_level_mapping = logging.getLevelNamesMapping()
    try:
        log_level = log_level_mapping[config.log.level]
    except KeyError:
        log_level = log_level_mapping["DEBUG"]
    logging.basicConfig(level=log_level, format=config.log.format)
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="locales/{locale}/"),
        default_locale="en",
        manager=UserManager(),
    )
    dp = Dispatcher(storage=storage)
    dp = Dispatcher()
    dp.include_routers(
        others.router,
        lang.router,
        user.router,
    )
    i18n_middleware.setup(dispatcher=dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
