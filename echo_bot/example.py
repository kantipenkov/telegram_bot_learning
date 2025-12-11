import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, and_f
from aiogram.types import Message, ContentType, ChatMemberUpdated

from filters import IsAdmin

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
try:
    ADMINS: list[int] = list(map(int, os.getenv('ADMINS', '').split(sep=',')))
except TypeError:
    ADMINS = []

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(and_f(IsAdmin(ADMINS), Command(commands='start')))
async def process_start_admin(message: Message):
    await message.answer('Admin?')

@dp.message(Command(commands='start'))
async def process_start_help(message: Message):
    await message.answer('Hell I\'m an echo bot. type something...')

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Send me a message and I\'ll echo it back')

# @dp.message(F.content_type == ContentType.PHOTO) # long version
@dp.message(F.photo)
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

@dp.message(F.sticker)
async def send_sticker_echo(message:Message):
    await message.reply_sticker(message.sticker.file_id)


@dp.message()
async def send_echo(message: Message):
    if message.text:
        await message.reply(text=message.text)
    else:
        await message.reply(text='Unknown input type')


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f"User {event.from_user.id} blocked the bot")

if __name__ == '__main__':
    dp.run_polling(bot)