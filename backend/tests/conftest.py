import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import SessionFactory, get_db
from app.domains.users.model import User
from app.core.security import hash_password


@pytest.fixture
async def db_session():
    async with SessionFactory() as session:
        yield session
        await session.rollback()


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


@pytest.fixture
async def test_user(db_session):
    user = User(
        name="testuser",
        email="test@example.com",
        hashed_password=hash_password("password"),
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    return user