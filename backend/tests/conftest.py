import os
import pytest

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.session import SessionFactory, engine
from app.domains.users.model import User
from app.core.security import hash_password


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")




@pytest.fixture
async def db_session():
    async with engine.connect() as conn:
        trans = await conn.begin()

        session = SessionFactory(bind=conn)

        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


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
        email="test@example.com",
        hashed_password=hash_password("password"),
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()   # commit禁止（重要）
    await db_session.refresh(user)

    return user