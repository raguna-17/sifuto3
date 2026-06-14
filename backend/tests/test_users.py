import pytest


# ==================================================
# register
# ==================================================

async def test_register_success(client):
    res = await client.post(
        "/users/register",
        json={
            "email": "a@example.com",
            "password": "password123"
        },
    )

    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "a@example.com"


# ==================================================
# register duplicate
# ==================================================

async def test_register_duplicate(client):
    await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123"
        },
    )

    res = await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123"
        },
    )

    assert res.status_code == 400
    assert "Email already exists" in res.json()["detail"]


# ==================================================
# login success
# ==================================================

async def test_login_success(client):
    await client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        },
    )

    res = await client.post(
        "/users/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        },
    )

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data


# ==================================================
# login fail
# ==================================================

async def test_login_fail(client):
    res = await client.post(
        "/users/login",
        json={
            "email": "notfound@example.com",
            "password": "wrongpassword"
        },
    )

    assert res.status_code == 401
    assert "Invalid email or password" in res.json()["detail"]


# ==================================================
# me endpoint
# ==================================================

async def test_me(client):
    res = await client.get("/users/me")

    assert res.status_code == 200
    data = res.json()

    assert data["email"] == "test@example.com"
    assert data["role"] == "ADMIN"
