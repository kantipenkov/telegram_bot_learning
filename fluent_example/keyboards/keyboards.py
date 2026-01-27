from aiogram.types import InlineKeyboardButton
from aiogram_i18n import LazyProxy
from aiogram_i18n.context import I18nContext
from aiogram_i18n.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

router_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=LazyProxy("help", case="capital"))]],
    resize_keyboard=True,
)


def get_language_menu_kb(
    i18n: I18nContext, markup_lang: str | None
) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = list()
    lang_buttons: list[InlineKeyboardButton] = list()
    for locale in i18n.core.available_locales:
        lang_buttons.append(
            InlineKeyboardButton(
                text=i18n.get("%s-lang" % (locale,)),
                callback_data=locale,
            )
        )
    buttons.append(lang_buttons)
    buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("cancel", markup_lang), callback_data="cancel_lang"
            ),
            InlineKeyboardButton(
                text=i18n.get("save", markup_lang), callback_data="save_lang"
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
