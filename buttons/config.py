from dataclasses import dataclass
import os

from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass()
class Config:
    bot: TgBot
    log: LogSettings


def _load_config() -> Config:
    path: str | None = os.getenv("CONFIG_PATH", None)
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env("BOT_TOKEN"), admins=env.list("ADMINS", subcast=int)),
        log=LogSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT")),
    )


config = _load_config()
