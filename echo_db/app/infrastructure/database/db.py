import logging
from datetime import datetime, timezone
from typing import Any

from psycopg import AsyncConnection
from psycopg.abc import Params, QueryNoTemplate
from psycopg.rows import Row, TupleRow

from app.bot.enums.roles import UserRole

logger = logging.getLogger(__name__)


async def execute_query(
    conn: AsyncConnection, query: QueryNoTemplate, params: Params
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(query=query, params=params)


async def fetch_all(
    conn: AsyncConnection, query: QueryNoTemplate, params: Params
) -> list[TupleRow] | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(query=query, params=params)
        row = await data.fetchall()
    return row


async def fetch_one(
    conn: AsyncConnection, query: QueryNoTemplate, params: Params
) -> TupleRow | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(query=query, params=params)
        row = await data.fetchone()
    return row


async def add_user(
    conn: AsyncConnection,
    *,
    user_id: int,
    username: str | None = None,
    language: str = "ru",
    role: UserRole = UserRole.USER,
    is_alive: bool = True,
    banned: bool = False
) -> None:
    await execute_query(
        conn,
        query="""
            INSERT INTO users(user_id, username, language, role, is_alive, banned)
            VALUES(
                %(user_id)s, 
                %(username)s, 
                %(language)s, 
                %(role)s, 
                %(is_alive)s, 
                %(banned)s
            ) ON CONFLICT DO NOTHING;
            """,
        params={
            "user_id": user_id,
            "username": username,
            "language": language,
            "role": role,
            "is_alive": is_alive,
            "banned": banned,
        },
    )
    logger.info(
        "User added. Table= '%s', user_id=%d, created_at='%s, "
        "language='%s', role='%s', is_alive=%s, banned=%s",
        "users",
        user_id,
        datetime.now(timezone.utc),
        language,
        role,
        is_alive,
        banned,
    )


async def get_user(conn: AsyncConnection, *, user_id: int) -> tuple[Any, ...] | None:
    row = await fetch_one(
        conn,
        query="""
            SELECT 
                id,
                user_id,
                username,
                language,
                role,
                is_alive,
                banned,
                created_at
                FROM users WHERE user_id = %s;
        """,
        params=(user_id,),
    )
    logger.info("Got user %s", row)
    return row if row else None


async def change_user_alive_status(
    conn: AsyncConnection, *, is_alive: bool, user_id: int
) -> None:
    await execute_query(
        conn,
        query="""UPDATE users SET is_alive = %s WHERE user_id = %s""",
        params=(is_alive, user_id),
    )
    logger.info("Updated 'is_alive' status to %s for user %d", is_alive, user_id)


async def change_user_banned_status_by_id(
    conn: AsyncConnection, *, banned: bool, user_id: int
) -> None:
    await execute_query(
        conn,
        query="UPDATE users SET banned = %s WHERE user_id = %s",
        params=(banned, user_id),
    )
    logger.info("Updated 'banned' status to '%s' for user %s", banned, user_id)


async def change_user_banned_status_by_username(
    conn: AsyncConnection, *, banned: bool, username: str
) -> None:
    await execute_query(
        conn,
        query="UPDATE users SET banned =  %s WHERE username = %s",
        params=(banned, username),
    )
    logger.info("Updated 'banned' status to '%s' for user %s", banned, username)


async def update_user_lang(
    conn: AsyncConnection, *, language: str, user_id: int
) -> None:
    await execute_query(
        conn,
        query="UPDATE users SET language = %s WHERE user_id = %s",
        params=(language, user_id),
    )
    logger.info("Update user languge to '%s' for user %d", language, user_id)


async def get_user_lang(conn: AsyncConnection, *, user_id: int) -> str | None:
    row = await fetch_one(
        conn, query="SELECT language FROM users WHERE user_id = %s", params=(user_id,)
    )
    if row:
        logger.info("The user's %s has the language is '%s'", user_id, row[0])
    else:
        logger.warning(
            "Can't fetch language for user '%s'. No entries for this user in db",
            user_id,
        )
    return row[0] if row else None


async def get_user_alive_status(conn: AsyncConnection, *, user_id: int) -> bool | None:
    row = await fetch_one(
        conn, query="SELECT is_alive FROM users WHERE user_id = %s", params=(user_id,)
    )
    if row:
        logger.info("User's %s is_alive status is %s", user_id, row[0])
    else:
        logger.warning(
            "Can't get is_alive status for user %s. No entry for this user yet.",
            user_id,
        )
    return row[0] if row else None


async def get_user_banned_status_by_user_id(
    conn: AsyncConnection, *, user_id: int
) -> bool | None:
    row = await fetch_one(
        conn, query="SELECT banned FROM users WHERE user_id = %s", params=(user_id,)
    )
    if row:
        logger.info("User's %s banned status is %s", user_id, row[0])
    else:
        logger.warning(
            "Can't get banned status for user %s. No entry for this user yet.",
            user_id,
        )
    return row[0] if row else None


async def get_user_banned_status_by_username(
    conn: AsyncConnection, *, username: str
) -> bool | None:
    row = await fetch_one(
        conn, query="SELECT banned FROM users WHERE username = %s", params=(username,)
    )
    if row:
        logger.info("User's %s banned status is %s", username, row[0])
    else:
        logger.warning(
            "Can't get banned status for user %s. No entry for this user yet.",
            username,
        )
    return row[0] if row else None


async def get_user_role(conn: AsyncConnection, *, user_id: int) -> str | None:
    row = await fetch_one(
        conn, query="SELECT role FROM users WHERE user_id = %s", params=(user_id,)
    )
    if row:
        logger.info("User's %s role is %s", user_id, row[0])
    else:
        logger.warning(
            "Can't get role for user %s. No entry for this user yet.",
            user_id,
        )
    return row[0] if row else None


async def add_user_activity(conn: AsyncConnection, *, user_id: int) -> None:
    await execute_query(
        conn,
        query="""INSERT INTO activity (user_id) VALUES(%s)
                ON CONFLICT (user_id, activity_date) DO UPDATE SET actions = activity.actions + 1""",
        params=(user_id,),
    )
    logger.info("Updated user activity for user '%s'", user_id)


async def get_statistics(conn: AsyncConnection) -> list[Any] | None:
    rows = await fetch_all(
        conn,
        query="SELECT user_id, SUM(actions) AS total_actions "
        "FROM activity GROUP BY user_id Order By total_actions DESC LIMIT 5",
        params=(),
    )
    logger.info("Fetched users activity from db")
    return [*rows] if rows else None
