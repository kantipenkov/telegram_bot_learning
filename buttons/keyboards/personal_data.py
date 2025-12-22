from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.command_start import home_btn
from lexicon import Commands

kb_builder = ReplyKeyboardBuilder()

location_btn = KeyboardButton(text=f"/{Commands.LOCATION}", request_location=True)
contact_btn = KeyboardButton(text=f"/{Commands.CONTACT}", request_contact=True)
user_id_btn = KeyboardButton(text=f"/{Commands.USER_ID}")

kb_builder.add(home_btn, location_btn, contact_btn, user_id_btn)
kb_builder.adjust(1, 3)
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
