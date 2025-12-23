import logging
import re
from string import ascii_lowercase

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InaccessibleMessage, Message

from keyboards.inline_buttons import OptionCallbackFactory, keyboard
from lexicon import Commands

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


# if you want to catch different options in different handlers you can set up filter like this:
# @router.callback_query(OptionCallbackFactory.filter(F.letter == "a"))
@router.callback_query(OptionCallbackFactory.filter())
async def inline_option(callback: CallbackQuery, callback_data: OptionCallbackFactory):
    logger.debug(f"Option {callback_data.letter.upper()} is clicked")
    if not isinstance(callback.message, InaccessibleMessage) and callback.message.text:
        text = callback.message.text
        scores = {
            k: int(v)
            for k, v in re.findall(
                r"Option (\w) clicked (\d+) times", callback.message.text
            )
        }

        scores[callback_data.letter.upper()] += 1
        await callback.message.edit_text(
            text=text_template % tuple(scores.values()),
            reply_markup=callback.message.reply_markup,
        )
    await callback.answer(
        text=f"button with option {callback_data.letter} is clicked"
    )  # this shows a popup


@router.callback_query(F.data == "reset")
async def reset_click(callback: CallbackQuery):
    logger.debug("Reset is clicked")
    if not isinstance(callback.message, InaccessibleMessage) and callback.message.text:
        if callback.message.text != text_template % (0, 0):
            await callback.message.edit_text(
                text=text_template % (0, 0), reply_markup=callback.message.reply_markup
            )
        await callback.answer(text="Reset button is clicked.")
