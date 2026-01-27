import logging

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n.context import I18nContext

from filters.filters import LangFilter
from keyboards.keyboards import get_language_menu_kb
from states import LanguageState

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("language_menu"))
async def lang_menu(message: Message, i18n: I18nContext, state: FSMContext) -> None:
    kb = get_language_menu_kb(i18n, i18n.core.get_locale())
    await state.set_state(LanguageState.language_selection)
    await message.answer(i18n.get("select-language"), reply_markup=kb)


@router.callback_query(StateFilter(LanguageState.language_selection), LangFilter())
async def language_selected(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext
) -> None:
    await state.update_data(selected_lang=callback.data)
    kb = get_language_menu_kb(i18n, markup_lang=callback.data)
    if callback.message and isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(
                text=i18n.get("select-language", callback.data), reply_markup=kb
            )
        except Exception as e:
            logger.exception(e)


@router.callback_query(
    StateFilter(LanguageState.language_selection), F.data == "cancel_lang"
)
async def calcel_language_selection(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext
):
    await state.update_data(selected_lang=None)
    await state.set_state()
    if callback.message and isinstance(callback.message, Message):
        await callback.message.edit_text(text=i18n.get("select-language-cancel"))


@router.callback_query(
    StateFilter(LanguageState.language_selection), F.data == "save_lang"
)
async def save_selected_language(
    callback: CallbackQuery, i18n: I18nContext, state: FSMContext
):
    context_data = await state.get_data()
    locale_code = context_data.get("selected_lang")
    if not locale_code:
        locale_code = i18n.core.get_locale()
    await state.update_data(selected_lang=None)
    await state.set_state()
    await i18n.set_locale(locale_code)
    if callback.message and isinstance(callback.message, Message):
        await callback.message.edit_text(
            text=i18n.get("select-language-save", language=locale_code)
        )
    await callback.answer()
