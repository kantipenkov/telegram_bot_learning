from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class OptionCallbackFactory(CallbackData, prefix="option", sep="_"):
    letter: str


# option_a_btn = InlineKeyboardButton(
#     text="Option A", callback_data=OptionCallbackFactory(letter="a").pack()
# )
# option_b_btn = InlineKeyboardButton(
#     text="Option B", callback_data=OptionCallbackFactory(letter="b").pack()
# )
# reset_btn = InlineKeyboardButton(text="Reset", callback_data="reset")
# home_btn = InlineKeyboardButton(text="Go Home", callback_data="Home")

kb_builder = InlineKeyboardBuilder()
# kb_builder.add(option_a_btn, option_b_btn, reset_btn, home_btn)
# we can do the same with builder's built-in methods
kb_builder.button(text="Option A", callback_data=OptionCallbackFactory(letter="a"))
kb_builder.button(text="Option B", callback_data=OptionCallbackFactory(letter="b"))
kb_builder.button(text="Reset", callback_data="reset")
kb_builder.button(text="Go Home", callback_data="Home")
kb_builder.adjust(2, 1)
keyboard: InlineKeyboardMarkup = kb_builder.as_markup()
