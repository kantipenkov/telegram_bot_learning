from aiogram.types import BotCommand

from app.bot.enums.roles import UserRole


def get_main_menu_commands(i18n: dict[str, str], role: UserRole):
    if role == UserRole.USER:
        return [
            BotCommand(
                command="/start", description=i18n.get("/start_description", "error")
            ),
            BotCommand(
                command="/lang", description=i18n.get("/lang_description", "error")
            ),
            BotCommand(
                command="/help", description=i18n.get("/help_description", "error")
            ),
        ]
    elif role == UserRole.ADMIN:
        return [
            BotCommand(
                command="/start", description=i18n.get("/start_description", "error")
            ),
            BotCommand(
                command="/lang", description=i18n.get("/lang_description", "error")
            ),
            BotCommand(
                command="/help", description=i18n.get("/help_description", "error")
            ),
            BotCommand(
                command="/ban", description=i18n.get("/ban_description", "error")
            ),
            BotCommand(
                command="/unban", description=i18n.get("/unban_description", "error")
            ),
            BotCommand(
                command="/statistics",
                description=i18n.get("/statistics_description", "error"),
            ),
        ]
