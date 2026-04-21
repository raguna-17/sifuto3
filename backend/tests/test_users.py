import pytest
from httpx import AsyncClient
from app.main import app


BASE_URL = "http://test"


# -------------------------
# ユーザー登録（正常系）
# -------------------------
@pytest.mark.asyncio
async def test_register_user_success():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        res = await ac.post(
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
    assert "hashed_password" not in data


# -------------------------
# 重複登録（異常系）
# -------------------------
@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # 1回目
        await ac.post(
            "/users/register",
            json={
                "email": "dup@example.com",
                "password": "password123",
            },
        )

        # 2回目（失敗）
        res = await ac.post(
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
async def test_login_success():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        await ac.post(
            "/users/register",
            json={
                "email": "login@example.com",
                "password": "password123",
            },
        )

        res = await ac.post(
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
async def test_login_fail_wrong_password():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        await ac.post(
            "/users/register",
            json={
                "email": "fail@example.com",
                "password": "password123",
            },
        )

        res = await ac.post(
            "/users/login",
            json={
                "email": "fail@example.com",
                "password": "wrongpass",
            },
        )

    assert res.status_code == 401


# -------------------------
# /me 成功（認証あり）
# -------------------------
@pytest.mark.asyncio
async def test_get_me_success():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # register
        await ac.post(
            "/users/register",
            json={
                "email": "me@example.com",
                "password": "password123",
            },
        )

        # login
        login_res = await ac.post(
            "/users/login",
            json={
                "email": "me@example.com",
                "password": "password123",
            },
        )

        token = login_res.json()["access_token"]

        # me
        res = await ac.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"


# -------------------------
# /me 認証なし（異常系）
# -------------------------
@pytest.mark.asyncio
async def test_get_me_unauthorized():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        res = await ac.get("/users/me")

    assert res.status_code == 401