import pytest

BASE_URL = "/api/v1/companies"


# =========================
# 正常系
# =========================

@pytest.mark.asyncio
async def test_get_companies(client, auth_headers, test_company):
    res = await client.get(BASE_URL + "/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    names = [c["name"] for c in data]
    assert test_company.name in names


@pytest.mark.asyncio
async def test_get_company_detail(client, auth_headers, test_company):
    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()

    assert data["id"] == test_company.id
    assert data["name"] == test_company.name


@pytest.mark.asyncio
async def test_create_company(client, auth_headers):
    payload = {
        "name": "New Company",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    assert res.status_code == 201
    data = res.json()

    assert data["name"] == payload["name"]
    assert data["industry"] == payload["industry"]


@pytest.mark.asyncio
async def test_delete_company(client, auth_headers, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}", headers=auth_headers)
    assert res.status_code == 204

    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)
    assert res.status_code == 404


# =========================
# 異常系
# =========================

@pytest.mark.asyncio
async def test_get_companies_unauthorized(client):
    res = await client.get(BASE_URL + "/")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_company_not_found(client, auth_headers):
    res = await client.get(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_company_invalid_id(client, auth_headers):
    res = await client.get(f"{BASE_URL}/invalid", headers=auth_headers)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_company_invalid_payload(client, auth_headers):
    payload = {
        "name": "",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_company_missing_field(client, auth_headers):
    payload = {
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_delete_company_not_found(client, auth_headers):
    res = await client.delete(f"{BASE_URL}/999999", headers=auth_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_company_unauthorized(client):
    payload = {
        "name": "Unauthorized Company",
        "industry": "IT"
    }

    res = await client.post(BASE_URL + "/", json=payload)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_delete_company_unauthorized(client, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}")
    assert res.status_code == 401


# 重複データ（fixtureに依存しない）
@pytest.mark.asyncio
async def test_create_company_duplicate(client, auth_headers, db_session):
    from app.models import Company

    # 先に作る（これが重要）
    company = Company(name="Duplicate Company", industry="IT")
    db_session.add(company)
    await db_session.commit()

    payload = {
        "name": "Duplicate Company",
        "industry": "IT"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    assert res.status_code in (400, 409)