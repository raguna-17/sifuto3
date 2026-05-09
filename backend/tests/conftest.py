import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import get_db, AsyncSessionLocal


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


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
    ) as ac:
        yield ac


'''
今回の原因を一文で言うなら：

pytest-asyncio が作る複数event loop間で、SQLAlchemy async connection poolを共有していた

そして修正は：

テスト環境では NullPool にして connection を使い回さない
'''