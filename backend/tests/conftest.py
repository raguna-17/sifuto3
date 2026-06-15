import os
import asyncio
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.domains.users.model import User
from app.db.session import get_db
from app.core.security import hash_password


# =========================
# DB URL
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# =========================
# event loop固定
# =========================
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


# =========================
# engine（同期fixture）
# =========================
@pytest.fixture(scope="session")
def engine():
    return create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


# =========================
# DB connection + transaction
# =========================
@pytest.fixture
async def connection(engine):
    async with engine.connect() as conn:
        trans = await conn.begin()
        try:
            yield conn
        finally:
            await trans.rollback()
            await conn.close()


# =========================
# session（このテスト単位で独立）
# =========================
@pytest.fixture
async def db_session(connection):
    SessionLocal = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with SessionLocal() as session:
        yield session


# =========================
# FastAPI client override
# =========================
@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import AsyncClient, ASGITransport

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# =========================
# test user
# =========================
@pytest.fixture
async def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password"),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user