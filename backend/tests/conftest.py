import pytest
import asyncio
import os

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.base import Base
from app.db.session import get_db
from app.main import app

from app.core.dependencies import get_current_user
from app.domains.users.model import User
from app.core.enums import UserRole
from app.core.security import hash_password


# ==================================================
# DB (CIのDATABASE_URLをそのまま使用)
# ==================================================
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ==================================================
# DB setup / teardown
# ==================================================
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ==================================================
# override DB session
# ==================================================
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# ==================================================
# override current user（テスト用固定ユーザー）
# ==================================================
async def override_current_user():
    return User(
        id=1,
        email="test@example.com",
        hashed_password=hash_password("password"),
        role=UserRole.ADMIN,
        is_active=True,
    )


app.dependency_overrides[get_current_user] = override_current_user


# ==================================================
# HTTP client
# ==================================================
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac


# ==================================================
# DB session fixture（必要時のみ）
# ==================================================
@pytest.fixture
async def db():
    async with TestingSessionLocal() as session:
        yield session