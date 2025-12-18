from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands import Commands
from keyboards.command_start import home_btn

kb_builder = ReplyKeyboardBuilder()

location_btn = KeyboardButton(text="/location", request_location=True)
contact_btn = KeyboardButton(text="/contact", request_contact=True)
user_id_btn = KeyboardButton(text=f"/{Commands.USER_ID}")

kb_builder.add(home_btn, location_btn, contact_btn, user_id_btn)
kb_builder.adjust(1, 3)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
