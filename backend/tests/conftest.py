import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import Base, get_db
import os


DATABASE_URL = os.getenv("DATABASE_URL")


# ----------------------------------
# engineを fixture内で作る（重要）
# ----------------------------------
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        DATABASE_URL,
        future=True,
        pool_pre_ping=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


# ----------------------------------
# session maker
# ----------------------------------
@pytest.fixture
def sessionmaker(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# ----------------------------------
# DB session（完全分離）
# ----------------------------------
@pytest.fixture
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session


# ----------------------------------
# client（毎回DBセッション新規）
# ----------------------------------
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