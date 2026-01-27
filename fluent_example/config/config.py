import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str
    admins: list[int]


@dataclass
class DbSettings:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    username: str
    password: str


@dataclass
class LoggingSettings:
    level: str
    format: str


@dataclass
class Config:
    bot: BotSettings
    db: DbSettings
    redis: RedisSettings
    log: LoggingSettings


def load_settings(path: str | None = None) -> Config:
    if not path:
        path = os.getenv("CONFIG_PATH", None)
    env = Env()
    env.read_env(path)

    bot = BotSettings(token=env("BOT_TOKEN"), admins=env.list("ADMINS", subcast=int))
    db = DbSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )
    redis = RedisSettings(
        host=env("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        username=env("REDIS_USERNAME"),
        password=env("REDIS_PASSWORD"),
    )
    log_settings = LoggingSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT"))
    config = Config(bot=bot, db=db, redis=redis, log=log_settings)
    return config


config = load_settings()
