from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# @router.message(F.content_type == ContentType.PHOTO) # long version
@router.message(F.photo)
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

@router.message(F.sticker)
async def send_sticker_echo(message:Message):
    await message.reply_sticker(message.sticker.file_id)


@router.message()
async def send_echo(message: Message):
    if message.text:
        await message.reply(text=message.text)
    else:
        await message.reply(text='Unknown input type')
