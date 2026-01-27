from typing import Any

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram_i18n import LazyProxy
from aiogram_i18n.context import I18nContext

router = Router()
router.message.filter(StateFilter(default_state))


@router.message(Command("help"))
@router.message(F.text == LazyProxy("help", case="capital"))
@router.message(F.text == LazyProxy("help", case="lower"))
async def help_cmd(message: Message, i18n: I18nContext) -> Any:
    if message.text:
        await message.reply(i18n.get("help-message"))


@router.message()
async def handler_common(message: Message, i18n: I18nContext) -> None:
    await message.answer(text=i18n.get("i-dont-know"))
    await message.answer(text=i18n.get("show-date", date_=message.date))
