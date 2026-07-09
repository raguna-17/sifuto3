import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from datetime import datetime, timedelta, UTC
from app.main import app
from app.db.session import get_db as app_get_db
from app.domains.users.model import User
from app.domains.shift_slots.model import ShiftSlot
from app.core.security import hash_password
from app.core.enums import UserRole
from app.core.config import get_settings


settings = get_settings()


# ==================================================
# TEST ENGINE（本番と完全分離）
# ==================================================
TEST_ENGINE = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionFactory = async_sessionmaker(
    bind=TEST_ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ==================================================
# override dependency
# ==================================================

async def override_get_db():
    async with TestSessionFactory() as session:
        try:
            yield session
        finally:
            await session.rollback()


# ==================================================
# API CLIENT FIXTURE
# ==================================================
@pytest.fixture
async def client():
    app.dependency_overrides[app_get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ==================================================
# DB SESSION FIXTURE（単体テスト用）
# ==================================================
@pytest.fixture
async def db_session():
    async with TestSessionFactory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# ==================================================
# TEST USER
# ==================================================
@pytest.fixture
async def test_user():

    async with TestSessionFactory() as session:

        user = User(
            name="testuser",
            email="test@example.com",
            hashed_password=hash_password("password"),
            is_active=True,
            role=UserRole.ADMIN,  # ←これ重要
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        yield user

        await session.delete(user)
        await session.commit()


# ==================================================
# AUTH HEADER
# ==================================================
@pytest.fixture
async def auth_headers(client, test_user):

    res = await client.post(
        "/users/login",
        json={
            "email": test_user.email,
            "password": "password",
        },
    )

    token = res.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
async def test_slot():

    async with TestSessionFactory() as session:

        slot = ShiftSlot(
            start_at=datetime.now(UTC),
            end_at=datetime.now(UTC) + timedelta(hours=8),
            required_staff_count=1,
        )

        session.add(slot)
        await session.commit()
        await session.refresh(slot)

        yield slot

        await session.delete(slot)
        await session.commit()