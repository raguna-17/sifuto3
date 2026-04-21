import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db import get_db, engine, Base


# -----------------------------
# テスト用DBセッション
# -----------------------------
@pytest.fixture
async def db_session():
    connection = await engine.connect()
    trans = await connection.begin()

    session = AsyncSession(bind=connection)

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


# -----------------------------
# FastAPIのDB依存をoverride
# -----------------------------
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