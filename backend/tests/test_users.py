import pytest
import uuid


def unique(prefix: str):
    return f"{prefix}_{uuid.uuid4()}@example.com"


# -------------------------
# 登録成功
# -------------------------
@pytest.mark.asyncio
async def test_register_user_success(client):
    email = unique("reg")

    res = await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    assert res.status_code == 200
    assert res.json()["email"] == email


# -------------------------
# 重複登録
# -------------------------
@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    email = unique("dup")

    await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    res = await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    assert res.status_code == 400


# -------------------------
# ログイン成功
# -------------------------
@pytest.mark.asyncio
async def test_login_success(client):
    email = unique("login")

    await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    res = await client.post(
        "/users/login",
        json={"email": email, "password": "password123"},
    )

    assert res.status_code == 200
    assert "access_token" in res.json()


# -------------------------
# ログイン失敗
# -------------------------
@pytest.mark.asyncio
async def test_login_fail_wrong_password(client):
    email = unique("fail")

    await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    res = await client.post(
        "/users/login",
        json={"email": email, "password": "wrongpass"},
    )

    assert res.status_code == 401


# -------------------------
# /me
# -------------------------
@pytest.mark.asyncio
async def test_get_me_success(client):
    email = unique("me")

    await client.post(
        "/users/register",
        json={"email": email, "password": "password123"},
    )

    login = await client.post(
        "/users/login",
        json={"email": email, "password": "password123"},
    )

    token = login.json()["access_token"]

    res = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert res.json()["email"] == email


# -------------------------
# 未認証
# -------------------------
@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    res = await client.get("/users/me")
    assert res.status_code == 401