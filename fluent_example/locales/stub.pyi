from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    items: Items

    @staticmethod
    def welcome(*, username: PossibleValue) -> Literal["""Добро пожаловать, { $username }!"""]: ...
    @staticmethod
    def help() -> Literal["""Помогите!"""]: ...

class Items:
    @staticmethod
    def count(*, count: PossibleValue) -> Literal["""у вас { $count } штук"""]: ...
