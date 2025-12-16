from aiogram import Router
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED
from aiogram.types import Message, ChatMemberUpdated

router = Router()

@router.message(Command(commands='start'))
async def process_start_help(message: Message):
    await message.answer('Hell I\'m an echo bot. type something...')

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Send me a message and I\'ll echo it back')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f"User {event.from_user.id} blocked the bot")
