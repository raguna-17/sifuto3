import asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import get_db, AsyncSessionLocal


# event loop（これ残す）
@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


# ⭐ここが重要：async fixtureやめる
@pytest.fixture
def client():
    transport = ASGITransport(app=app)

    return AsyncClient(
        transport=transport,
        base_url="http://test",
    )