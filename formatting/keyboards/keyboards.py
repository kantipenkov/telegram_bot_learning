from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb_builder = InlineKeyboardBuilder()
kb_builder.button(text="HTML", callback_data="html_style")
kb_builder.button(text="Markdown", callback_data="markdown_style")
kb_builder.adjust(2)

keyboard: InlineKeyboardMarkup = kb_builder.as_markup()
