import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()


# will handle only if .start command sent and fsm is in default state
@router.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    await message.answer(
        text="This is an example that shows FSM form fill. To start send command /fillform"
    )


@router.message(Command(commands="help"))
async def help(message: Message):
    await message.answer(
        text="This is a simple example of work with FSM."
        "To start send command /fillform."
        "To cancel filling in the form send /cancel"
    )
