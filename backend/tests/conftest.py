import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import Base, get_db
import os


# -----------------------------------
# 環境変数は「読むだけ」
# -----------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")


# -----------------------------------
# テスト専用Engine（本番と完全分離）
# -----------------------------------
test_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -----------------------------------
# DB初期化（テスト全体で1回）
# -----------------------------------
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -----------------------------------
# DBセッション（各テストごと）
# -----------------------------------
@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# -----------------------------------
# FastAPI Test Client
# -----------------------------------
@pytest.fixture
async def client(db_session):
    # DI override
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    # cleanup（必ず戻す）
    app.dependency_overrides.clear()