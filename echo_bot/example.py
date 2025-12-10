import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands='start'))
async def process_start_help(message: Message):
    await message.answer('Hell I\'m an echo bot. type something...')

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Send me a message and I\'ll echo it back')

@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)