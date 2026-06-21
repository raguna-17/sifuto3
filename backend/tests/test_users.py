import pytest


# =========================
# register
# =========================
@pytest.mark.asyncio
async def test_register_success(client):

    payload = {
        "email": "newuser@example.com",
        "password": "password123"
    }

    res = await client.post("/users/register", json=payload)
    print(res.json())
    assert res.status_code == 201

    data = res.json()

    assert data["email"] == payload["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, test_user):

    payload = {
        "email": test_user.email,
        "password": "password123"
    }

    res = await client.post("/users/register", json=payload)

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already exists"


# =========================
# login
# =========================
@pytest.mark.asyncio
async def test_login_success(client, test_user):

    payload = {
        "email": test_user.email,
        "password": "password"
    }

    res = await client.post("/users/login", json=payload)

    assert res.status_code == 200

    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data  # サービス仕様に合わせる


@pytest.mark.asyncio
async def test_login_invalid_email(client):

    payload = {
        "email": "notfound@example.com",
        "password": "password"
    }

    res = await client.post("/users/login", json=payload)

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):

    payload = {
        "email": test_user.email,
        "password": "wrongpassword"
    }

    res = await client.post("/users/login", json=payload)

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid email or password"


# =========================
# me
# =========================
@pytest.mark.asyncio
async def test_read_current_user_success(client, auth_headers):

    res = await client.get("/users/me", headers=auth_headers)

    assert res.status_code == 200

    data = res.json()

    assert "email" in data
    assert "id" in data


@pytest.mark.asyncio
async def test_read_current_user_no_token(client):

    res = await client.get("/users/me")

    assert res.status_code == 401