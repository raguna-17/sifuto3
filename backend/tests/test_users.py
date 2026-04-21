import pytest


# -------------------------
# ユーザー登録（正常系）
# -------------------------
@pytest.mark.asyncio
async def test_register_user_success(client):
    res = await client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert res.status_code == 200
    data = res.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "is_active" in data


# -------------------------
# 重複登録（異常系）
# -------------------------
@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123",
        },
    )

    res = await client.post(
        "/users/register",
        json={
            "email": "dup@example.com",
            "password": "password123",
        },
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"


# -------------------------
# ログイン成功
# -------------------------
@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    res = await client.post(
        "/users/login",
        json={
            "email": "login@example.com",
            "password": "password123",
        },
    )

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# -------------------------
# ログイン失敗（異常系）
# -------------------------
@pytest.mark.asyncio
async def test_login_fail_wrong_password(client):
    await client.post(
        "/users/register",
        json={
            "email": "fail@example.com",
            "password": "password123",
        },
    )

    res = await client.post(
        "/users/login",
        json={
            "email": "fail@example.com",
            "password": "wrongpass",
        },
    )

    assert res.status_code == 401


# -------------------------
# /me 正常系（認証あり）
# -------------------------
@pytest.mark.asyncio
async def test_get_me_success(client):
    await client.post(
        "/users/register",
        json={
            "email": "me@example.com",
            "password": "password123",
        },
    )

    login_res = await client.post(
        "/users/login",
        json={
            "email": "me@example.com",
            "password": "password123",
        },
    )

    token = login_res.json()["access_token"]

    res = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"


# -------------------------
# /me 異常系（未認証）
# -------------------------
@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    res = await client.get("/users/me")

    assert res.status_code == 401