from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.command_start import home_btn

_dogs_button = KeyboardButton(text="Dogs")
_cucumbers_button = KeyboardButton(text="Cucumbers")

_kb_builder = ReplyKeyboardBuilder()
_kb_builder.row(_dogs_button, _cucumbers_button)
_kb_builder.row(home_btn)
_kb_builder.adjust(2, 1)
keyboard: ReplyKeyboardMarkup = _kb_builder.as_markup(
    resize_keyboard=True
)
