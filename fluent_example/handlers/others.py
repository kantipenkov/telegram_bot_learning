from typing import Any

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram_i18n.context import I18nContext

from keyboards.keyboards import router_kb

router = Router()
router.message.filter(StateFilter(default_state))


@router.message(CommandStart())
async def start_cmd(message: Message, i18n: I18nContext) -> Any:
    name = message.from_user.mention_html()
    await message.reply(
        text=i18n.get("hello", user=name, language=i18n.locale), reply_markup=router_kb
    )
