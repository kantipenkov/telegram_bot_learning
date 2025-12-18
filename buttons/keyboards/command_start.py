from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands import BUTTONS_EXAMPLE, POLL_EXAMPLE

# dogs_button = KeyboardButton(text="Dogs")
# cucumbers_button = KeyboardButton(text="Cucumbers")
home_btn = KeyboardButton(text="Home")
_buttons_example = KeyboardButton(text=f"/{BUTTONS_EXAMPLE}")
_poll_example = KeyboardButton(text=f"/{POLL_EXAMPLE}")

_kb_builder = ReplyKeyboardBuilder()
_kb_builder.add(home_btn)
_kb_builder.add(_buttons_example, _poll_example)
_kb_builder.adjust(1, 3)
keyboard: ReplyKeyboardMarkup = _kb_builder.as_markup(
    resize_keyboard=True, one_time_keyboard=True
)
