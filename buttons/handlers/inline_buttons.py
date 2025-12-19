import logging
import re
from string import ascii_lowercase
from typing import Final, Literal

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InaccessibleMessage, Message

from commands import Commands
from keyboards.inline_buttons import keyboard

logger = logging.getLogger(__name__)
router = Router()


text_template = """This is an example of inline buttons. Choose you option or go to Start.\nResults:
Option A clicked %s times.
Option B clicked %s times"""


@router.message(Command(commands=Commands.INLINE_BUTTONS_EXAMPLE))
async def inline_buttons_example(message: Message):
    await message.answer(
        text=text_template % (0, 0),
        reply_markup=keyboard,
    )


def create_option_callback(letter: str) -> None:
    if len(letter) == 1 and letter.lower() == letter and letter in ascii_lowercase:

        @router.callback_query(F.data == f"option_{letter}")
        async def option_click(callback: CallbackQuery):
            logger.debug(f"Option {letter.upper} is clicked")
            if (
                not isinstance(callback.message, InaccessibleMessage)
                and callback.message.text
            ):
                text = callback.message.text
                nums = list(map(int, re.findall(r"(\d+) times", text)))
                nums[list(ascii_lowercase).index(letter.lower())] += 1
                await callback.message.edit_text(
                    text=text_template % tuple(nums),
                    reply_markup=callback.message.reply_markup,
                )
            await callback.answer(text=f"button with option {letter} is clicked")

        # return option_click
    else:
        raise ValueError(
            "Input %s is invalid. Please pass single lowercase letter" % letter,
        )


@router.callback_query(F.data == "reset")
async def reset_click(callback: CallbackQuery):
    logger.debug("Reset is clicked")
    if not isinstance(callback.message, InaccessibleMessage) and callback.message.text:
        if callback.message.text != text_template % (0, 0):
            await callback.message.edit_text(
                text=text_template % (0, 0), reply_markup=callback.message.reply_markup
            )
        await callback.answer(text="Reset button is clicked.")


create_option_callback("a")
create_option_callback("b")
