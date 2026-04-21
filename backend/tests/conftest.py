import asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


# -----------------------------
# event loop を固定（超重要）
# -----------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# -----------------------------
# http client fixture
# -----------------------------
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac