from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(msg: Message):
    await msg.answer("test")


@router.message()
async def echo(msg: Message):
    if isinstance(msg, Message) and msg.text:
        await msg.answer(msg.text)
