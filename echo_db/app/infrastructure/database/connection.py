import logging
from urllib.parse import quote

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


def build_pg_conn_info(
    db_name: str, host: str, port: int, user: str, password: str
) -> str:
    conn_info = (
        f"postgresql://{quote(user, safe="")}:{quote(password, safe="")}"
        f"@{host}:{port}/{db_name}"
    )
    logger.debug("Building PostgreSQL connection url")
    return conn_info


async def log_db_version(connection: AsyncConnection) -> None:
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT version();")
            db_version = await cursor.fetchone()
            logger.info(f"Connected to PostgreSQL version: {db_version[0]}")
    except Exception as e:
        logger.warning("Failed to fetch DB version", e)


async def get_pg_connection(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
    min_size: int = 1,
    max_size: int = 3,
    timeout: float = 10.0,
) -> AsyncConnection:
    conn_info = build_pg_conn_info(db_name, host, port, user, password)
    connection: AsyncConnection | None = None
    try:
        connection = await AsyncConnection.connect(conninfo=conn_info)
        await log_db_version(connection)
        return connection
    except Exception as e:
        logger.exception("Failed to connect to PostgreSQL: %s", e)
        if connection:
            await connection.close()
        raise


async def get_pg_pool(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
    min_size: int = 1,
    max_size: int = 3,
    timeout: float = 10.0,
) -> AsyncConnectionPool:
    conn_info = build_pg_conn_info(db_name, host, port, user, password)
    db_pool: AsyncConnectionPool | None = None
    try:
        db_pool = AsyncConnectionPool(
            conninfo=conn_info,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            open=False,
        )
        await db_pool.open()
        async with db_pool.connection() as conn:
            await log_db_version(conn)
        return db_pool
    except Exception as e:
        logger.exception("Failed to initialize PostgreSQL pool: %s", e)
        if db_pool and not db_pool.closed:
            await db_pool.close()
        raise
