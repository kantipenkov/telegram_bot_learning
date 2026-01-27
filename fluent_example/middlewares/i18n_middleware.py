from aiogram.types import User
from aiogram_i18n.managers import BaseManager


# add db and implement cache somewhere
class UserManager(BaseManager):
    # this a workaround because I don't have db
    locale_storage: dict[str, str]

    def __init__(self, default_locale: str | None = None) -> None:
        self.locale_storage = dict()
        super().__init__(default_locale)

    async def get_locale(self, event_from_user: User, **kwargs) -> str:
        default = event_from_user.language_code or self.default_locale
        # try getting lang from db
        if str(event_from_user.id) in self.locale_storage:
            return self.locale_storage[str(event_from_user.id)]
        return default or "en"

    async def set_locale(self, locale: str, event_from_user: User, **kwargs) -> None:
        # set lang to db
        self.locale_storage[str(event_from_user.id)] = locale
