from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

gender_kb_builder = InlineKeyboardBuilder()
gender_kb_builder.button(text="Male", callback_data="male")
gender_kb_builder.button(text="Female", callback_data="female")
gender_kb_builder.button(text="Don't know", callback_data="undefined")
gender_kb_builder.adjust(2)

gender_keyboard: InlineKeyboardMarkup = gender_kb_builder.as_markup()

edu_kb_builder = InlineKeyboardBuilder()
edu_kb_builder.button(text="Only school", callback_data="secondary")
edu_kb_builder.button(text="University", callback_data="higher")
edu_kb_builder.button(text="No education", callback_data="no_edu")

education_kb: InlineKeyboardMarkup = edu_kb_builder.as_markup()

yes_no_kb_builder = InlineKeyboardBuilder()
yes_no_kb_builder.button(text="Yes", callback_data="yes")
yes_no_kb_builder.button(text="No", callback_data="no")
yes_no_kb_builder.adjust(2)

yes_no_kb: InlineKeyboardMarkup = yes_no_kb_builder.as_markup()
