from sqlalchemy import create_engine
from alembic import context
from src.core.settings import get_settings
from src.db import models
from src.db.models import Base

settings = get_settings()
config = context.config
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", settings.DB.make_url("postgresql"))

def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction() as transaction:
            context.run_migrations()
            if "dry-run" in context.get_x_argument():
                print(
                    "Dry-run succeeded; now rolling back transaction..."
                )  # noqa: T201
                transaction.rollback()
    connectable.dispose()


run_migrations_online()