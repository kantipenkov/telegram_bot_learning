from dataclasses import dataclass
from enum import StrEnum, auto


class Commands(StrEnum):
    BUTTONS_EXAMPLE = auto()
    POLL_EXAMPLE = auto()
    CAT_POLL = auto()
    PERSONAL_DATA = auto()
    SHARED_USERS = auto()
    INLINE_BUTTONS_EXAMPLE = auto()
    USER_ID = auto()
    SELECT_USER = auto()
    SELECT_USERS = auto()
    SELECT_CHAT = auto()
    LOCATION = auto()
    CONTACT = auto()


# LEXICON = {"home_banner": "Choose the demo", "": ""}


@dataclass(frozen=True, slots=True)
class Lexicon:
    home_banner: str = "Choose the demo"
    cat_question: str = "What cats are more afraid of?"
    cat_dog: str = "Dogs"
    cat_cucumber: str = "Cucumbers"
    cat_dog_answer: str = (
        "Yes, cats are afraid of dogs but have you ever seen how they are afraid of cucumbers."
    )
    cat_cucumber_answer: str = "Yes, sometimes cats are afraid of cucumbers a lot."
    quiz: str = "Create quiz"
    poll: str = "Create poll"
    poll_quiz: str = "Create poll/quiz"
    poll_banner: str = "What operation with polls do you want to execute?"
    personal_phone: str = "Your telephone number: "
    personal_location: str = "Your location is: "
    tg_user_id: str = "Your telegram user id is: "
    personal_data_banner: str = "Receiving personal data demo"
    shared_user_banner: str = "Select what to share"


lexicon = Lexicon()
