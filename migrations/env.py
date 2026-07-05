import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# 1. Inject the 'src' directory into the Python path so Alembic can find your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 2. Import your Base metadata, models, and system configuration variables
from database import Base
from auth.models import User  # Forces the User model to register in memory
from config import settings as db_settings  # Adjust this import name to match where your config class resides

# This is the config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Point target_metadata directly to your combined Base metadata registry
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Dynamically read your secure asyncpg URL instead of hardcoding it in alembic.ini
    url = db_settings.ASYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context."""

    # Explicitly spawn the engine utilizing your settings database URL
    connectable = create_async_engine(
        db_settings.ASYNC_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()