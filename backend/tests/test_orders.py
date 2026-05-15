import pytest
from sqlalchemy import text

from app.db.session import AsyncSessionLocal


# =========================================================
# helper
# =========================================================

async def create_admin_user(client):

    # register
    await client.post(
        "/users/register",
        json={
            "email": "admin@example.com",
            "password": "password123"
        }
    )

    # admin化
    async with AsyncSessionLocal() as session:
        await session.execute(
            text(
                """
                UPDATE users
                SET role='admin'
                WHERE email='admin@example.com'
                """
            )
        )
        await session.commit()

    # login
    login_res = await client.post(
        "/users/login",
        json={
            "email": "admin@example.com",
            "password": "password123"
        }
    )

    token = login_res.json()["access_token"]

    return token


async def create_normal_user(client, email="user@example.com"):

    await client.post(
        "/users/register",
        json={
            "email": email,
            "password": "password123"
        }
    )

    login_res = await client.post(
        "/users/login",
        json={
            "email": email,
            "password": "password123"
        }
    )

    return login_res.json()["access_token"]


async def create_product(client, admin_token):

    res = await client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "sample product",
            "price": 1000,
            "stock": 10
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    return res.json()


# =========================================================
# 注文作成成功
# =========================================================

@pytest.mark.asyncio
async def test_create_order_success(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(client)

    res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["total_price"] == 2000
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["status"] == "pending"


# =========================================================
# 在庫不足
# =========================================================

@pytest.mark.asyncio
async def test_create_order_insufficient_stock(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="stock@example.com"
    )

    res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 999
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert res.status_code == 400


# =========================================================
# 自分の注文一覧
# =========================================================

@pytest.mark.asyncio
async def test_get_my_orders(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="orders@example.com"
    )

    await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    res = await client.get(
        "/orders/",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert len(data) >= 1


# =========================================================
# 注文詳細取得
# =========================================================

@pytest.mark.asyncio
async def test_get_order_detail(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="detail@example.com"
    )

    create_res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_res.json()["id"]

    res = await client.get(
        f"/orders/{order_id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == order_id


# =========================================================
# 管理者：ステータス更新
# =========================================================

@pytest.mark.asyncio
async def test_update_order_status_success(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="status@example.com"
    )

    create_res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_res.json()["id"]

    res = await client.patch(
        f"/orders/admin/{order_id}/status",
        json={
            "status": "paid"
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["status"] == "paid"


# =========================================================
# 不正な状態遷移
# =========================================================

@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="invalid@example.com"
    )

    create_res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_res.json()["id"]

    # pending → shipped は禁止
    res = await client.patch(
        f"/orders/admin/{order_id}/status",
        json={
            "status": "shipped"
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert res.status_code == 404 or res.status_code == 400


# =========================================================
# 管理者：削除
# =========================================================

@pytest.mark.asyncio
async def test_delete_order_success(client):

    admin_token = await create_admin_user(client)

    product = await create_product(client, admin_token)

    user_token = await create_normal_user(
        client,
        email="delete@example.com"
    )

    create_res = await client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 1
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_res.json()["id"]

    res = await client.delete(
        f"/orders/admin/{order_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["message"] == "deleted"