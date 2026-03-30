import pytest

BASE_URL = "/api/v1/applications"

async def test_get_my_applications(client, auth_headers, test_application):
    res = await client.get(f"{BASE_URL}/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["position"] == test_application.position


async def test_get_application_detail(client, auth_headers, test_application):
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_application.id
    assert data["position"] == test_application.position


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


async def test_delete_application(client, auth_headers, test_application):
    res = await client.delete(f"{BASE_URL}/{test_application.id}", headers=auth_headers)

    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)
    assert res.status_code == 404