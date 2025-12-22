from aiogram.types import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestUsers,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.command_start import home_btn
from lexicon import Commands

kb_builder = ReplyKeyboardBuilder()
request_user_btn = KeyboardButton(
    text=f"/{Commands.SELECT_USER}",
    request_user=KeyboardButtonRequestUser(request_id=42, user_is_premium=False),
)

request_users_btn = KeyboardButton(
    text=f"/{Commands.SELECT_USERS}",
    request_users=KeyboardButtonRequestUsers(
        request_id=43, user_is_premium=False, max_quantity=3
    ),
)

request_chat_btn = KeyboardButton(
    text=f"/{Commands.SELECT_CHAT}",
    request_chat=KeyboardButtonRequestChat(
        request_id=44, chat_is_channel=False, chat_is_forum=False
    ),
)

kb_builder.add(home_btn, request_user_btn, request_users_btn, request_chat_btn)
kb_builder.adjust(1, 3)

keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
