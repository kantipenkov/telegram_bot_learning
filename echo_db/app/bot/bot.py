import logging

import psycopg_pool
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot.handlers import admin, others, settings, user
from app.bot.i18n.translator import get_translations
from app.bot.middlewares import (
    ActivityCounterMiddleware,
    DataBaseMiddleware,
    LangSettingsMiddleware,
    ShadowBanMiddleware,
    TranslatorMiddleware,
)
from app.infrastructure.database.connection import get_pg_pool
from config import Config

logger = logging.getLogger(__name__)


async def main(config: Config):
    logger.info("Starting the bot...")
    bot = Bot(config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis = Redis(
        host="redis",
        port=config.redis.port,
        db=config.redis.db,
        password=config.redis.password,
        username=config.redis.username,
    )
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )
    translations = get_translations()
    locales = list(translations.keys())
    # add routers
    dp.include_routers(settings.router, admin.router, user.router, others.router)
    # add middlewares
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(ShadowBanMiddleware())
    dp.update.middleware(ActivityCounterMiddleware())
    dp.update.middleware(LangSettingsMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    try:
        await dp.start_polling(
            bot,
            config=config,
            db_pool=db_pool,
            translations=translations,
            locales=locales,
            admin_ids=config.bot.admins,
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.debug("Postgres connection closed")
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    dp.include_routers(others.router)
    await dp.start_polling(bot, config=config)
    await dp.start_polling(bot, config=config)
