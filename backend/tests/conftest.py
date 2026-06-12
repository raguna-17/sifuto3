import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import get_db, SessionFactory


# =========================
# DB override
# =========================
async def override_get_db():
    async with SessionFactory() as session:
        yield session


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


# =========================
# HTTP client
# =========================
@pytest.fixture
def client():
    return AsyncClient(
        transport=ASGITransport(app=app, lifespan="on"),
        base_url="http://test",
    )


# =========================
# pytest async mode
# =========================
pytestmark = pytest.mark.anyio