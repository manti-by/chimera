import asyncio
import threading
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from chimera.settings import DB_URL


def get_async_engine(echo: bool = False, isolation_level: str = "AUTOCOMMIT") -> AsyncEngine:
    return create_async_engine(DB_URL, echo=echo, isolation_level=isolation_level)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    async_session_maker = get_async_session_maker(engine)
    async with async_session_maker() as session:
        yield session


def get_sync_engine(echo: bool = False, isolation_level: str = "AUTOCOMMIT"):
    return create_engine(DB_URL.replace("asyncpg", "psycopg"), echo=echo, isolation_level=isolation_level)


_engine_cache: dict[tuple[int, str], AsyncEngine] = {}
_cache_lock = threading.Lock()


async def get_cached_engine(db_name: str | None = None) -> AsyncEngine:
    loop_id = id(asyncio.get_running_loop())
    key = (loop_id, db_name or "default")
    if key not in _engine_cache:
        with _cache_lock:
            if key not in _engine_cache:
                _engine_cache[key] = get_async_engine()
    return _engine_cache[key]


@asynccontextmanager
async def get_connection(db_name: str | None = None) -> AsyncGenerator[AsyncSession]:
    engine = await get_cached_engine(db_name)
    async with AsyncSession(engine) as session:
        yield session
