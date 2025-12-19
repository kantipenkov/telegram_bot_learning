from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

option_a_btn = InlineKeyboardButton(text="Option A", callback_data="option_a")
option_b_btn = InlineKeyboardButton(text="Option B", callback_data="option_b")
reset_btn = InlineKeyboardButton(text="Reset", callback_data="reset")
home_btn = InlineKeyboardButton(text="Go Home", callback_data="go_home")

kb_builder = InlineKeyboardBuilder()
kb_builder.add(option_a_btn, option_b_btn, reset_btn, home_btn)
kb_builder.adjust(2, 1)
keyboard: InlineKeyboardMarkup = kb_builder.as_markup()
