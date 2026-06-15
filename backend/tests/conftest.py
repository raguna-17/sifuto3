import os
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db

from app.domains.users.model import User
from app.core.security import create_access_token, hash_password


# =========================
# DB URL
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# =========================
# engine
# =========================
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        DATABASE_URL,
        future=True,
        echo=False,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


# =========================
# db session
# =========================
@pytest.fixture
async def db_session(engine):
    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestingSessionLocal() as session:
        yield session


# =========================
# override dependency
# =========================
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


# =========================
# auth headers
# =========================
@pytest.fixture
async def auth_headers(test_user):

    token = create_access_token({
        "sub": str(test_user.id),
        "role": test_user.role.value,  # Enum安全化
    })

    return {
        "Authorization": f"Bearer {token}"
    }