import pytest

BASE_URL = "/api/v1/applications"

# =========================
# 正常系
# =========================

@pytest.mark.asyncio
async def test_get_my_applications(client, auth_headers, test_application):
    res = await client.get(f"{BASE_URL}/", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["position"] == test_application.position

@pytest.mark.asyncio
async def test_get_application_detail(client, auth_headers, test_application):
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_application.id
    assert data["position"] == test_application.position

@pytest.mark.asyncio
async def test_create_application(client, auth_headers):
    payload = {
        "company_name": "Create Test Co",
        "industry": "IT",
        "position": "Frontend Engineer"
    }
    res = await client.post(f"{BASE_URL}/", json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["position"] == "Frontend Engineer"
    assert data["company"]["name"] == "Create Test Co"

@pytest.mark.asyncio
async def test_delete_application(client, auth_headers, test_application):
    res = await client.delete(f"{BASE_URL}/{test_application.id}", headers=auth_headers)
    assert res.status_code == 204
    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)
    assert res.status_code == 404

# =========================
# 異常系
# =========================

# 認証なしアクセス
@pytest.mark.asyncio
async def test_get_my_applications_unauthorized(client):
    res = await client.get(f"{BASE_URL}/")
    assert res.status_code == 401

# 存在しないID参照
@pytest.mark.asyncio
async def test_get_application_not_found(client, auth_headers):
    res = await client.get(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404

# 不正ID（型エラー）
@pytest.mark.asyncio
async def test_get_application_invalid_id(client, auth_headers):
    res = await client.get(f"{BASE_URL}/invalid", headers=auth_headers)
    assert res.status_code == 422

# 作成時バリデーションエラー
@pytest.mark.asyncio
async def test_create_application_invalid_payload(client, auth_headers):
    payload = {
        "company_name": "",
        "industry": "IT",
        "position": "Frontend Engineer"
    }
    res = await client.post(f"{BASE_URL}/", json=payload, headers=auth_headers)
    assert res.status_code == 422

# 削除：存在しないID
@pytest.mark.asyncio
async def test_delete_application_not_found(client, auth_headers):
    res = await client.delete(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404

# 認証なしで作成・削除
@pytest.mark.asyncio
async def test_create_application_unauthorized(client):
    payload = {
        "company_name": "Unauthorized Co",
        "industry": "IT",
        "position": "Frontend Engineer"
    }
    res = await client.post(f"{BASE_URL}/", json=payload)
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_delete_application_unauthorized(client, test_application):
    res = await client.delete(f"{BASE_URL}/{test_application.id}")
    assert res.status_code == 401