"""Alembic environment configuration for async SQLAlchemy.

This script sets up Alembic to run migrations against the async
SQLAlchemy engine defined in the application. It imports the
`Base` metadata from `app.models` so that `alembic revision --autogenerate`
can detect model changes.
"""

import sys
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Ensure the project root is on sys.path so imports work.
sys.path.append(".")

# Load the Alembic configuration.
config = context.config

# Enable logging from the config file if present.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the Base metadata from the application.
from app.models import Base

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in offline mode.

    No DB connection is required; Alembic emits SQL scripts.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in online mode using the async engine.

    Alembic expects a synchronous connection, so we create an async engine
    and then obtain its synchronous proxy via `engine.sync_engine`.
    """
    from app.config import settings
    # Create an async engine from the async DB URL.
    async_engine = create_async_engine(settings.DB_URL, future=True)
    # Obtain the synchronous wrapper for Alembic.
    sync_engine = async_engine.sync_engine
    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
