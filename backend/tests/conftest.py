import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import SessionFactory, get_db
from app.domains.users.model import User
from app.core.security import hash_password


# -------------------------
# API Client
# -------------------------
@pytest.fixture
async def client():

    async def override_get_db():
        async with SessionFactory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# -------------------------
# DB Session
# -------------------------
@pytest.fixture
async def db_session():
    async with SessionFactory() as session:
        try:
            yield session
        finally:
            await session.rollback()


# -------------------------
# Test User
# -------------------------
@pytest.fixture
async def test_user():

    async with SessionFactory() as session:

        user = User(
            name="testuser",
            email="test@example.com",
            hashed_password=hash_password("password"),
            is_active=True,
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        yield user

        await session.delete(user)
        await session.commit()