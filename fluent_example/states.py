from aiogram.fsm.state import State, StatesGroup


class LanguageState(StatesGroup):
    language_selection = State()
