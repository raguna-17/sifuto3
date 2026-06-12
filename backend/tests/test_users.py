import pytest



async def test_register_success(client):
    response = await client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data



async def test_register_duplicate_email(client):
    await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123"
        }
    )

    res = await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123"
        }
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"



async def test_login_success(client):
    await client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    res = await client.post(
        "/users/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"



async def test_login_invalid_password(client):
    await client.post(
        "/users/register",
        json={
            "email": "wrongpass@example.com",
            "password": "password123"
        }
    )

    res = await client.post(
        "/users/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"



async def test_me_success(client):
    await client.post(
        "/users/register",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )

    login_res = await client.post(
        "/users/login",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )

    token = login_res.json()["access_token"]

    res = await client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"



async def test_me_unauthorized(client):
    res = await client.get("/users/me")

    assert res.status_code == 401

