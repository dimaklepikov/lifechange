import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.db.database import Base
from app.models import user, task
from app.config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine

# this is the Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)
config.set_main_option('sqlalchemy.url', DATABASE_URL)

target_metadata = Base.metadata

def get_engine():
    return async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        pool_pre_ping=True,
        future=True,
    )
print("🧠 TABLES IN MODELS:", target_metadata.tables.keys())
async def run_migrations():
    connectable = create_async_engine(DATABASE_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_migrations())


if context.is_offline_mode():
    raise NotImplementedError("Offline mode not supported in async setup")
else:
    run_migrations_online()