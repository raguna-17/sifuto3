import pytest

BASE_URL = "/api/v1/companies"

async def test_get_companies(client, auth_headers, test_company):
    res = await client.get(BASE_URL + "/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Test Company"


async def test_get_company_detail(client, auth_headers, test_company):
    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_company.id
    assert data["name"] == "Test Company"


async def test_create_company(client, auth_headers):
    payload = {
        "name": "New Company",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "New Company"
    assert data["industry"] == "Finance"


async def test_delete_company(client, auth_headers, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}", headers=auth_headers)

    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_company.id}", headers=auth_headers)
    assert res.status_code == 404