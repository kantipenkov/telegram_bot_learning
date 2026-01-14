import html
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, PhotoSize
from aiogram.utils.text_decorations import html_decoration

from fsm.fsm import FSMFillForm
from keyboards import education_kb, gender_keyboard, yes_no_kb

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def cancel_in_form(message: Message, state: FSMContext):
    await message.answer(
        text="Cancel filling in the form. Exit from FSM. If you wish to fill in the form send /fillform"
    )
    await state.clear()


@router.message(Command(commands="cancel"), StateFilter(default_state))
async def cancel_not_in_form(message: Message, state: FSMContext):
    await message.answer(
        text="Can't cancel filling in the form, you are not in the process of filling in one."
        "If you wish to fill in the form send /fillform"
    )


@router.message(Command(commands="fillform"), StateFilter(default_state))
async def fill_form(message: Message, state: FSMContext):
    await message.answer(text="Please enter your name")
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def fill_name(message: Message, state: FSMContext):
    await message.answer("Thank you. Enter your age please")
    await state.update_data(name=message.text)
    await state.set_state(FSMFillForm.fill_age)


@router.message(StateFilter(FSMFillForm.fill_name))
async def fill_name_err(message: Message):
    await message.answer(
        f"{message.text} is not a valid name. Please enter a valid name or exit the form with /cancel command."
    )


@router.message(
    StateFilter(FSMFillForm.fill_age),
    lambda x: x.text.isdigit() and 4 <= int(x.text) <= 100,
)
async def fill_age(message: Message, state: FSMContext):
    await message.answer(
        text="Thank you. Please select you gender now.", reply_markup=gender_keyboard
    )
    await state.update_data(age=message.text)
    await state.set_state(FSMFillForm.fill_gender)


@router.message(StateFilter(FSMFillForm.fill_age))
async def fill_age_err(message: Message):
    await message.answer(
        text=f"{message.text} is not a valid age. Age should be an integer between 4 and 100."
        "Please enter your age again or exit the form sending /cancel"
    )


@router.callback_query(
    StateFilter(FSMFillForm.fill_gender), F.data._in(["male", "female", "undefined"])
)
async def fill_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    if isinstance(callback.message, Message):
        await callback.message.answer(text="Thank you. Please upload your photo now.")
    await state.set_state(FSMFillForm.upload_photo)
    await callback.answer()


@router.message(StateFilter(FSMFillForm.fill_gender))
async def fill_gender_err(message: Message):
    await message.answer(
        text="Please use inline buttons under the message to choose your gender.",
        reply_markup=gender_keyboard,
    )


@router.message(StateFilter(FSMFillForm.upload_photo), F.photo[-1].as_("largest_photo"))
async def upload_photo(message: Message, state: FSMContext, largest_photo: PhotoSize):
    await state.update_data(
        photo_id=largest_photo.file_id, photo_unique_id=largest_photo.file_unique_id
    )
    await message.answer(
        text="Thank you. Please select your education level now.",
        reply_markup=education_kb,
    )
    await state.set_state(FSMFillForm.fill_education)


@router.message(StateFilter(FSMFillForm.upload_photo))
async def upload_photo_err(message: Message):
    await message.answer(
        "Please upload an image as your profile photo or exit the form sending /cancel"
    )


@router.callback_query(
    StateFilter(FSMFillForm.fill_education),
    F.data.in_(["secondary", "higher", "no_edu"]),
)
async def fill_education(callback: CallbackQuery, state: FSMContext):
    await state.update_data(education=callback.data)
    if isinstance(callback.message, Message):
        await callback.message.answer(
            "Thank you. Please tell us if you want to receive updates in messages.",
            reply_markup=yes_no_kb,
        )
    await state.set_state(FSMFillForm.fill_wish_news)
    await callback.answer()


@router.message(StateFilter(FSMFillForm.fill_education))
async def fill_education_err(message: Message):
    await message.answer(
        "Please choose your education level by clicking on one of inline buttons below the message or exit the form sending /cancel",
        reply_markup=education_kb,
    )


@router.callback_query(
    StateFilter(FSMFillForm.fill_wish_news), F.data.in_(["yes", "no"])
)
async def news_subscription(callback: CallbackQuery, state: FSMContext):
    await state.update_data(news=callback.data == "yes")
    if isinstance(callback.message, Message):
        user_data = await state.get_data()
        callback.message.answer_photo(
            photo=user_data["photo_id"],
            caption=f"Name: {user_data["name"]}"
            f"Age: {user_data["age"]}"
            f"Gender: {user_data["gender"]}"
            f"Education: {user_data["education"]}"
            f"Receive news: {user_data["news"]}",
        )
    await state.clear()
    await callback.answer()


@router.message(StateFilter(FSMFillForm.fill_wish_news))
async def news_subscription_err(message: Message):
    await message.answer(
        "Please choose if your wish to receive news by clicking on one of inline buttons below the message or exit the form sending /cancel",
        reply_markup=education_kb,
    )


@router.message(StateFilter(default_state))
async def unknown_message(message: Message):
    await message.answer("Unknown command. Please use /help")
