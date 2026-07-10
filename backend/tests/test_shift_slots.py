from datetime import datetime, timedelta, UTC

import pytest


@pytest.mark.asyncio
async def test_create_shift_slot(client, auth_headers):

    payload = {
        "start_at": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "end_at": (datetime.now(UTC) + timedelta(days=1, hours=8)).isoformat(),
        "required_staff_count": 2,
    }

    res = await client.post(
        "/shift-slots",
        headers=auth_headers,
        json=payload,
    )

    assert res.status_code == 201

    data = res.json()

    assert data["required_staff_count"] == 2
    assert "id" in data


@pytest.mark.asyncio
async def test_get_shift_slots(client):

    res = await client.get("/shift-slots")

    assert res.status_code == 200

    data = res.json()

    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_shift_slot(client, auth_headers):

    payload = {
        "start_at": (datetime.now(UTC) + timedelta(days=2)).isoformat(),
        "end_at": (datetime.now(UTC) + timedelta(days=2, hours=8)).isoformat(),
        "required_staff_count": 1,
    }

    created = await client.post(
        "/shift-slots",
        headers=auth_headers,
        json=payload,
    )

    slot_id = created.json()["id"]

    res = await client.get(f"/shift-slots/{slot_id}")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == slot_id


@pytest.mark.asyncio
async def test_update_shift_slot(client, auth_headers):

    payload = {
        "start_at": (datetime.now(UTC) + timedelta(days=3)).isoformat(),
        "end_at": (datetime.now(UTC) + timedelta(days=3, hours=8)).isoformat(),
        "required_staff_count": 1,
    }

    created = await client.post(
        "/shift-slots",
        headers=auth_headers,
        json=payload,
    )

    slot_id = created.json()["id"]

    update_payload = {
        "required_staff_count": 3
    }

    res = await client.patch(
        f"/shift-slots/{slot_id}",
        headers=auth_headers,
        json=update_payload,
    )

    assert res.status_code == 200

    data = res.json()

    assert data["required_staff_count"] == 3


@pytest.mark.asyncio
async def test_delete_shift_slot(client, auth_headers):

    payload = {
        "start_at": (datetime.now(UTC) + timedelta(days=4)).isoformat(),
        "end_at": (datetime.now(UTC) + timedelta(days=4, hours=8)).isoformat(),
        "required_staff_count": 1,
    }

    created = await client.post(
        "/shift-slots",
        headers=auth_headers,
        json=payload,
    )

    slot_id = created.json()["id"]

    res = await client.delete(
        f"/shift-slots/{slot_id}",
        headers=auth_headers,
    )

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_get_shift_slot_not_found(client):

    res = await client.get("/shift-slots/999999")

    assert res.status_code == 404