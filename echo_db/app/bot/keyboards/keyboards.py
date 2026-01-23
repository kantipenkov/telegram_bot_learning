from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_lang_settings_kb(
    i18n: dict[str, str], locales: list[str], checked: str
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for locale in sorted(locales):
        if locale == "default":
            continue
        if locale == checked:
            keyboard_builder.button(text=f"🔘 {i18n.get(locale)}", callback_data=locale)
        else:
            keyboard_builder.button(text=f"⚪️ {i18n.get(locale)}", callback_data=locale)
    keyboard_builder.adjust(1)
    keyboard_builder.row(
        InlineKeyboardButton(
            text=i18n.get("cancel_lang_button_text", "error"),
            callback_data="cancel_lang_button_data",
        ),
        InlineKeyboardButton(
            text=i18n.get("save_lang_button_text", "error"),
            callback_data="save_lang_button_data",
        ),
    )
    return keyboard_builder.as_markup()
