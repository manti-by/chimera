import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from chimera.database.tables import metadata
from chimera.settings import DB_URL


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline() -> None:
    url = make_url(DB_URL).render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = DB_URL.replace("%", "%%")
    config.set_main_option(name="sqlalchemy.url", value=url)

    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    asyncio.run(_run_async_migrations(connectable))


async def _run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata,
            )
        )

        def run_migrations(_conn):
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
