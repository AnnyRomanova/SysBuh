import pytest_asyncio

from src.db.session import DatabaseConnector
from src.db.models import Base


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:148989@localhost:5432/SysBuh_db"

@pytest_asyncio.fixture
async def test_db():
    db = DatabaseConnector(TEST_DATABASE_URL)

    async with db._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db

    async with db._engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db.disconnect()
