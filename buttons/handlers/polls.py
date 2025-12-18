import logging

from aiogram import F, Router
from aiogram.enums import PollType
from aiogram.filters import Command
from aiogram.types import Message, PollAnswer, TelegramObject

from commands import Commands
from keyboards.polls import keyboard

logger = logging.getLogger(__name__)
router = Router()


def dump(message: TelegramObject, prefix: str = "Created poll"):

    logger.debug("%s: %s", prefix, message.model_dump_json(indent=4, exclude_none=True))


@router.message(Command(commands=Commands.POLL_EXAMPLE))
async def poll_example(message: Message):
    await message.answer(
        text="What operation with polls do you want to execute?", reply_markup=keyboard
    )


# create cat poll
@router.message(Command(commands=Commands.CAT_POLL))
async def create_cat_poll(message: Message):
    await message.answer_poll(
        question="What cats are more afraid of?",
        options=["Dogs", "Cucumbers"],
        is_anonymous=False,
        type=PollType.REGULAR,
    )


# catch poll creation
@router.message(F.poll.type == PollType.REGULAR)
async def process_poll(message: Message):
    dump(message)
    # react to the poll with emoji
    await message.answer_poll(
        question=message.poll.question,
        options=[opt.text for opt in message.poll.options],
        is_anonymous=False,
        type=message.poll.type,
        allows_multiple_answers=message.poll.allows_multiple_answers,
        message_effect_id="5107584321108051014",
    )


@router.message(F.poll.type == PollType.QUIZ)
async def process_poll_quiz(message: Message):
    dump(message)
    await message.answer_poll(
        question=message.poll.question,
        options=[opt.text for opt in message.poll.options],
        is_anonymous=False,
        type=message.poll.type,
        correct_option_id=message.poll.correct_option_id,
        explanationf=message.poll.explanation,
        explanation_entities=message.poll.explanation_entities,
        message_effect_id="5104841245755180586",
    )


# only catches answers on non anonynous polls/quizzes
@router.poll_answer()
async def process_answer_poll(poll_answer: PollAnswer):
    dump(poll_answer, "poll answer received")
