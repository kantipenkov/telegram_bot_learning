import logging
from contextlib import suppress

from aiogram import Bot, F, Router
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BotCommandScopeChat,
    CallbackQuery,
    InaccessibleMessage,
    Message,
)
from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.bot.filters import LocaleFilter, UserRoleFilter
from app.bot.keyboards.keyboards import get_lang_settings_kb
from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG
from app.infrastructure.database.db import (
    get_user_lang,
    get_user_role,
    update_user_lang,
)

logger = logging.getLogger(__name__)

router = Router()


@router.message(StateFilter(LangSG.lang), ~CommandStart())
async def select_language_in_lang_state(
    msg: Message, bot: Bot, i18n: dict[str, str], state: FSMContext, locales: list[str]
):
    user_id = msg.from_user.id
    data = await state.get_data()
    user_lang = data.get("user_lang")
    if not user_lang:
        logger.error("Failed to get user_lang from FSMContext. Fallback to 'en'")
        user_lang = "en"

    with suppress(TelegramBadRequest):
        msg_id = data.get("lang_settings_msg_id")
        if msg_id:
            # remove klang keyboard from previous message because there should be only one at a time
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg_id)

    reply = await msg.answer(
        text=i18n.get("/lang", "error"),
        reply_markup=get_lang_settings_kb(
            i18n=i18n, locales=locales, checked=user_lang
        ),
    )

    await state.update_data(lang_settings_msg_id=reply.message_id, user_lang=user_lang)


@router.message(Command(commands="lang"))
async def command_lang(
    msg: Message,
    conn: AsyncConnection,
    i18n: dict[str, str],
    state: FSMContext,
    locales: list[str],
):
    await state.set_state(LangSG.lang)
    user_lang = await get_user_lang(conn, user_id=msg.from_user.id)
    if not user_lang:
        logger.warning("Failed to get user language settings from db. Fallback to 'en'")
        user_lang = "en"
    reply = await msg.answer(
        text=i18n.get("/lang", "error"),
        reply_markup=get_lang_settings_kb(
            i18n=i18n, locales=locales, checked=user_lang
        ),
    )
    await state.update_data(lang_settings_msg_id=reply.message_id, user_lang=user_lang)


@router.callback_query(F.data == "save_lang_button_data")
async def process_save_click(
    callback: CallbackQuery,
    bot: Bot,
    conn: AsyncConnection,
    i18n: dict[str, str],
    state: FSMContext,
):
    data = await state.get_data()
    await update_user_lang(
        conn, language=data.get("user_lang", ""), user_id=callback.from_user.id
    )
    if not isinstance(callback.message, InaccessibleMessage):
        await callback.message.edit_text(text=i18n.get("lang_saved", "error"))
    else:
        logger.warning("Can't edit message")

    user_role = await get_user_role(conn, user_id=callback.from_user.id)
    if not user_role:
        logger.error("Cant fetch user role from db.")
        raise Exception("Cant fetch user role from db.")
    if isinstance(user_role, str):
        user_role = UserRole(user_role)
    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n, role=user_role),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT, chat_id=callback.from_user.id
        ),
    )

    await state.update_data(lang_settings_msg_id=None, user_lang=None)
    await state.set_state()


@router.callback_query(F.data == "cancel_lang_button_data")
async def lang_cancel(
    callback: CallbackQuery,
    conn: AsyncConnection,
    i18n: dict[str, str],
    state: FSMContext,
):
    if not isinstance(callback.message, InaccessibleMessage):
        user_lang = await get_user_lang(conn, user_id=callback.from_user.id)
        if user_lang:
            await callback.message.edit_text(
                text=i18n.get("lang_cancelled", "").format(i18n.get(user_lang, "error"))
            )
        else:
            await callback.message.edit_text(
                text="Failed to get proper message from dictionary"
            )
        await state.update_data(lang_settings_msg_id=None, user_lang=None)
        await state.set_state()
    else:
        raise Exception("message inaccessible for %s" % (callback.id))


@router.callback_query(LocaleFilter())
async def process_lang_click(
    callback: CallbackQuery, i18n: dict[str, str], locales: list[str]
):
    try:
        if not isinstance(callback.message, InaccessibleMessage) and callback.data:
            await callback.message.edit_text(
                text=i18n.get("/lang", "error"),
                reply_markup=get_lang_settings_kb(
                    i18n=i18n, locales=locales, checked=callback.data
                ),
            )
    except TelegramBadRequest:
        await callback.answer()
