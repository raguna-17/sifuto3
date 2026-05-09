import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_register_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/register", json={
            "email": "test@example.com",
            "password": "password123"
        })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/register", json={
            "email": "dup@example.com",
            "password": "password123"
        })

        res = await ac.post("/users/register", json={
            "email": "dup@example.com",
            "password": "password123"
        })

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/register", json={
            "email": "login@example.com",
            "password": "password123"
        })

        res = await ac.post("/users/login", json={
            "email": "login@example.com",
            "password": "password123"
        })

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/register", json={
            "email": "wrongpass@example.com",
            "password": "password123"
        })

        res = await ac.post("/users/login", json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        })

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_me_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/users/register", json={
            "email": "me@example.com",
            "password": "password123"
        })

        login_res = await ac.post("/users/login", json={
            "email": "me@example.com",
            "password": "password123"
        })

        token = login_res.json()["access_token"]

        res = await ac.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_me_unauthorized():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/users/me")

    assert res.status_code == 401