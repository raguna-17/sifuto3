import os
import pytest_asyncio
import pytest
from argon2 import PasswordHasher
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main import app
from app.db.base import Base
from app.db.session import get_db

from app.domains.users.model import User
from app.core.enums import UserRole
from app.core.security import create_access_token


ph = PasswordHasher()
DATABASE_URL = os.getenv("DATABASE_URL")


@pytest_asyncio.fixture(scope="session")
async def engine():

    engine = create_async_engine(
        DATABASE_URL,
        future=True,
    )

    yield engine

    await engine.dispose()

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db_session(engine):

    async with engine.connect() as connection:

        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        try:
            yield session

        finally:
            await session.close()
            await transaction.rollback()


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def test_user(db_session):

    user = User(
        email="test@example.com",
        hashed_password=ph.hash("password123"),
        role=UserRole.USER,
        is_active=True,
    )

    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def auth_headers(test_user):

    token = create_access_token(
        {
            "sub": str(test_user.id),
            "role": test_user.role.value,
        }
    )

    return {
        "Authorization": f"Bearer {token}"
    }
