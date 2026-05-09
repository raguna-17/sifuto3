import pytest
from httpx import AsyncClient,ASGITransport

from app.main import app


# =========================
# ヘルパー
# =========================

REGISTER_URL = "/users/register"
LOGIN_URL = "/users/login"
ME_URL = "/users/me"


# =========================
# user register
# =========================

@pytest.mark.asyncio
async def test_register_success():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(REGISTER_URL, json={
            "email": "test@example.com",
            "password": "password123"
        })

    assert response.status_code == 200
    data = res.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(REGISTER_URL, json={
            "email": "dup@example.com",
            "password": "password123"
        })

        res = await ac.post(REGISTER_URL, json={
            "email": "dup@example.com",
            "password": "password123"
        })

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"


# =========================
# login
# =========================

@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(REGISTER_URL, json={
            "email": "login@example.com",
            "password": "password123"
        })

        res = await ac.post(LOGIN_URL, json={
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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(REGISTER_URL, json={
            "email": "wrongpass@example.com",
            "password": "password123"
        })

        res = await ac.post(LOGIN_URL, json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        })

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"


# =========================
# me endpoint
# =========================

@pytest.mark.asyncio
async def test_me_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register
        await ac.post(REGISTER_URL, json={
            "email": "me@example.com",
            "password": "password123"
        })

        # login
        login_res = await ac.post(LOGIN_URL, json={
            "email": "me@example.com",
            "password": "password123"
        })

        token = login_res.json()["access_token"]

        # me
        res = await ac.get(
            ME_URL,
            headers={"Authorization": f"Bearer {token}"}
        )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_me_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get(ME_URL)

    assert res.status_code == 401