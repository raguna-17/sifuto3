import os
import pytest
import uuid

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import get_db

from app.users.model import User
from app.recruiting.organizations.model import Organization
from app.recruiting.job_applications.model import JobApplication

from app.core.security import create_access_token

from argon2 import PasswordHasher

ph = PasswordHasher()

DATABASE_URL = os.getenv("DATABASE_URL")
@pytest.fixture
async def engine():
    engine = create_async_engine(
    DATABASE_URL
    )
    try:
        yield engine
    finally:
        await engine.dispose()

@pytest.fixture
async def db_session(engine):
    async with engine.connect() as connection:
        transaction = await connection.begin()

        TestingSessionLocal = sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        session = TestingSessionLocal()

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()




@pytest.fixture
async def client(db_session):

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):

    user = User(
        email="test@example.com",
        hashed_password=ph.hash("password"),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def test_organization(db_session):
    organization = Organization(
        name=f"Test Organization {uuid.uuid4()}",
        industry="IT"
    )

    db_session.add(organization)
    await db_session.commit()
    await db_session.refresh(organization)

    return organization


@pytest.fixture
async def test_job_application(db_session, test_user, test_organization):

    job_application = JobApplication(
        job_title="Backend Engineer",
        user_id=test_user.id,
        organization_id=test_organization.id
    )

    db_session.add(job_application)
    await db_session.commit()
    await db_session.refresh(job_application)

    return job_application

    


@pytest.fixture
async def auth_headers(test_user):

    token = create_access_token({
        "sub": str(test_user.id),
        "role": test_user.role,
    })

    return {
        "Authorization": f"Bearer {token}"
    }

