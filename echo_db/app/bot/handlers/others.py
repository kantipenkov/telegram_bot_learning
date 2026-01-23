from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from psycopg import AsyncConnection

router = Router()


# @router.message(CommandStart())
# async def start(msg: Message):
#     await msg.answer("test")


# @router.message()
# async def echo(msg: Message):
#     if isinstance(msg, Message) and msg.text:
#         await msg.answer(msg.text)


@router.message()
async def echo(msg: Message, conn: AsyncConnection, i18n: dict):
    try:
        await msg.send_copy(chat_id=msg.chat.id)
    except TypeError:
        await msg.reply(text=i18n.get("no_echo", "error"))
