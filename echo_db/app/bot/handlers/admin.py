import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.bot.filters import UserRoleFilter
from app.infrastructure.database.db import (
    change_user_banned_status_by_id,
    change_user_banned_status_by_username,
    get_statistics,
    get_user_banned_status_by_user_id,
    get_user_banned_status_by_username,
)

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(UserRoleFilter(UserRole.ADMIN))


@router.message(Command(commands="help"))
async def admin_help(msg: Message, i18n: dict[str, str]):
    await msg.answer(text=i18n.get("/help_admin", "error"))


@router.message(Command("statistics"))
async def admin_statistics(msg: Message, conn: AsyncConnection, i18n: dict[str, str]):
    statistics = await get_statistics(conn)
    if statistics:
        await msg.answer(
            text=i18n.get("statistics", "").format(
                "\n".join(
                    f"{i}. <b>{stat[0]}</b>: {stat[1]}"
                    for i, stat in enumerate(statistics, 1)
                )
            )
        )
    else:
        await msg.answer("Failed to get statistics")


@router.message(Command("ban"))
async def ban_user(
    msg: Message, conn: AsyncConnection, command: CommandObject, i18n: dict[str, str]
):
    args = command.args
    if not args:
        await msg.reply(i18n.get("empty_ban_answer", "Error"))

    arg_user = args.split()[0].strip()
    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_user_id(
            conn, user_id=int(arg_user)
        )
    elif arg_user.startswith("@"):
        banned_status = await get_user_banned_status_by_username(
            conn, username=arg_user[1:]
        )
    else:
        await msg.reply(text=i18n.get("incorrect_ban_arg", "error"))
        return
    if banned_status is None:
        await msg.reply(text=i18n.get("no_user", "error"))
    elif banned_status:
        await msg.reply(text=i18n.get("already_banned", "error"))
    else:
        if arg_user.isdigit():
            await change_user_banned_status_by_id(
                conn, banned=True, user_id=int(arg_user)
            )
        else:
            await change_user_banned_status_by_username(
                conn, banned=True, username=arg_user[1:]
            )
        await msg.reply(text=i18n.get("successfully_banned", "error"))


@router.message(Command("unban"))
async def unban_user(
    msg: Message, conn: AsyncConnection, command: CommandObject, i18n: dict[str, str]
):
    args = command.args
    if not args:
        await msg.reply(i18n.get("empty_unban_answer", "Error"))

    arg_user = args.split()[0].strip()
    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_user_id(
            conn, user_id=int(arg_user)
        )
    elif arg_user.startswith("@"):
        banned_status = await get_user_banned_status_by_username(
            conn, username=arg_user[1:]
        )
    else:
        await msg.reply(text=i18n.get("incorrect_ban_arg", "error"))
        return
    if banned_status is None:
        await msg.reply(text=i18n.get("no_user", "error"))
    elif banned_status:
        if arg_user.isdigit():
            await change_user_banned_status_by_id(
                conn, banned=False, user_id=int(arg_user)
            )
        else:
            await change_user_banned_status_by_username(
                conn, banned=False, username=arg_user[1:]
            )
        await msg.reply(text=i18n.get("successfully_banned", "error"))
    else:
        await msg.reply(text=i18n.get("not_banned", "error"))
