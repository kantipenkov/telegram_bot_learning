from aiogram.enums import PollType
from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.command_start import home_btn
from lexicon import Commands, lexicon

_kb_builder = ReplyKeyboardBuilder()

# poll creation

_poll_quiz_btn = KeyboardButton(
    text=lexicon.poll_quiz, request_poll=KeyboardButtonPollType()
)

_poll_btn = KeyboardButton(
    text=lexicon.poll, request_poll=KeyboardButtonPollType(type=PollType.REGULAR)
)
_quiz_btn = KeyboardButton(
    text=lexicon.quiz, request_poll=KeyboardButtonPollType(type=PollType.QUIZ)
)

_cat_poll = KeyboardButton(text=f"/{Commands.CAT_POLL}")

_kb_builder.row(_poll_quiz_btn, _poll_btn, _quiz_btn, _cat_poll)
_kb_builder.row(home_btn)

keyboard: ReplyKeyboardMarkup = _kb_builder.as_markup(resize_keyboard=True)
