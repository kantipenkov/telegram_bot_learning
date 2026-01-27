from typing import TYPE_CHECKING

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner
from fluentogram.storage.file import FileStorage

# if TYPE_CHECKING:
#     from locales.stub import TranslatorRunner

storage = FileStorage("locales/{locale}/")

locales_map = {
    "ru": (
        "ru",
        "en",
    ),  # this is a fallback if 'ru' locale can't be found than 'en' will be used
    "en": "en",
}
hub = TranslatorHub(
    locales_map,
    storage=storage,
)
translator: TranslatorRunner = hub.get_translator_by_locale("en")

print(translator.get("hello", user="Nick", language="test"))
print(translator.hello(user="Alice", language="test"))
# print(translator.get("items-count", count=5))
print(translator.get("help-message"))


def test():
    a = 12 + 3
    print("hello")
    print(a)
    print("привет")


if __name__ == "__main__":
    test()
