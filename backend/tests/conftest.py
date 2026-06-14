import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db, SessionFactory, engine


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def dispose_engine():
    yield
    await engine.dispose()


async def override_get_db():
    async with SessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()