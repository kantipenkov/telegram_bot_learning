import asyncio
import logging
import os
import sys

from psycopg import AsyncConnection, Error

from app.infrastructure.database.connection import get_pg_connection
from config.config import Config, config

log_level_mapping = logging.getLevelNamesMapping()
try:
    log_level = log_level_mapping[config.log.level]
except KeyError:
    log_level = log_level_mapping["DEBUG"]
logging.basicConfig(
    level=log_level,
    format=config.log.format,
)

logger = logging.getLogger(__name__)


async def main():
    connection: AsyncConnection | None = None

    try:
        connection = await get_pg_connection(
            db_name=config.db.name,
            host=config.db.host,
            port=config.db.port,
            user=config.db.user,
            password=config.db.password,
        )
        logger.info("Set up the db")
        async with connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        query="""
                            CREATE TABLE IF NOT EXISTS users(
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT NOT NULL UNIQUE,
                                username VARCHAR(50),
                                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                language VARCHAR(10) NOT NULL,
                                role VARCHAR(30) NOT NULL,
                                is_alive BOOLEAN NOT NULL,
                                banned BOOLEAN NOT NULL
                            ); 
                        """
                    )
                    await cursor.execute(
                        query="""
                            CREATE TABLE IF NOT EXISTS activity(
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT REFERENCES users(user_id),
                                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                activity_date DATE NOT NULL DEFAULT CURRENT_DATE,
                                actions INT NOT NULL DEFAULT 1
                            );
                            CREATE UNIQUE INDEX IF NOT EXISTS idx_activity_user_day
                            ON activity (user_id, activity_date);
                        """
                    )
                    logger.info("Added tables 'users' and 'activity'")
    except Error as db_error:
        logger.exception("DB error: %s", db_error)
    except Exception as e:
        logger.exception("Unhandled error: %s", e)
    finally:
        if connection:
            await connection.close()
            logger.info("Close db connection")
