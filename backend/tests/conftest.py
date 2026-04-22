import pytest
import asyncio
import os

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import Base, get_db


# ----------------------------------
# event loop固定（超重要）
# ----------------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ----------------------------------
# DB URL（CIから注入）
# ----------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")


# ----------------------------------
# テスト専用engine（pool無効化）
# ----------------------------------
test_engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ----------------------------------
# DB初期化
# ----------------------------------
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


# ----------------------------------
# DBセッション（テストごと）
# ----------------------------------
@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# ----------------------------------
# FastAPI client
# ----------------------------------
@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()