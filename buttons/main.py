from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from environs import Env

env = Env()
env.read_env()
BOT_TOKEN = env("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

button_1 = KeyboardButton(text="Dogs")
button_2 = KeyboardButton(text="Cucumbers")

keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2]],
    resize_keyboard=True,
    one_time_keyboard=True,  # this allows to hide keyboard automatically and retrieve it if user wishes by clicking on an icon
)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text="What cats are more afraid of?", reply_markup=keyboard)


@dp.message(F.text == "Cucumbers")
async def cucumbers_answer(message: Message):
    await message.answer(
        text="Yes, sometimes cats are afraid of cucumbers a lot.",
        # reply_markup=ReplyKeyboardRemove(), # remove keyboard completely
    )


@dp.message(F.text == "Dogs")
async def dogs_answer(message: Message):
    await message.answer(
        text="Yes, cats are afraid of dogs but have you ever seen how they are afraid of cucumbers.",
        # reply_markup=ReplyKeyboardRemove(),
    )


if __name__ == "__main__":
    dp.run_polling(bot)
