from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram_i18n.context import I18nContext


class LangFilter(BaseFilter):

    async def __call__(
        self, callback: CallbackQuery, i18n: I18nContext, *args: Any, **kwargs: Any
    ) -> Any:
        locales = i18n.core.available_locales
        return callback.data in locales
