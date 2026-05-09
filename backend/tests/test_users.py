import pytest


def test_register_success(client):
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post("/users/register", json={
        "email": "dup@example.com",
        "password": "password123"
    })

    res = client.post("/users/register", json={
        "email": "dup@example.com",
        "password": "password123"
    })

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"


def test_login_success(client):
    client.post("/users/register", json={
        "email": "login@example.com",
        "password": "password123"
    })

    res = client.post("/users/login", json={
        "email": "login@example.com",
        "password": "password123"
    })

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post("/users/register", json={
        "email": "wrongpass@example.com",
        "password": "password123"
    })

    res = client.post("/users/login", json={
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    })

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"


def test_me_success(client):
    client.post("/users/register", json={
        "email": "me@example.com",
        "password": "password123"
    })

    login_res = client.post("/users/login", json={
        "email": "me@example.com",
        "password": "password123"
    })

    token = login_res.json()["access_token"]

    res = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"


def test_me_unauthorized(client):
    res = client.get("/users/me")
    assert res.status_code == 401