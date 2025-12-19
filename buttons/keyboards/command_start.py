from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands import Commands

# dogs_button = KeyboardButton(text="Dogs")
# cucumbers_button = KeyboardButton(text="Cucumbers")
home_btn = KeyboardButton(text="Home")
_buttons_example = KeyboardButton(text=f"/{Commands.BUTTONS_EXAMPLE}")
_poll_example = KeyboardButton(text=f"/{Commands.POLL_EXAMPLE}")
_personal_data_example = KeyboardButton(text=f"/{Commands.PERSONAL_DATA}")
_shared_users_example = KeyboardButton(text=f"/{Commands.SHARED_USERS}")

_kb_builder = ReplyKeyboardBuilder()
_kb_builder.add(home_btn)
_kb_builder.add(
    _buttons_example, _poll_example, _personal_data_example, _shared_users_example
)
_kb_builder.adjust(1, 4)
keyboard: ReplyKeyboardMarkup = _kb_builder.as_markup(
    resize_keyboard=True, one_time_keyboard=True
)
