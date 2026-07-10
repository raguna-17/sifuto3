from datetime import datetime, timedelta, UTC

import pytest

from app.core.enums import PreferencePriority


# ==================================================
# Create
# ==================================================
@pytest.mark.asyncio
async def test_create_preference(
    client,
    auth_headers,
    test_slot,
):
    payload = {
        "shift_slot_id": test_slot.id,
        "priority": PreferencePriority.PREFERRED.value,
        "note": "希望します",
    }

    res = await client.post(
        "/shift-preferences",
        headers=auth_headers,
        json=payload,
    )

    assert res.status_code == 201

    data = res.json()

    assert data["shift_slot_id"] == test_slot.id
    assert data["priority"] == PreferencePriority.PREFERRED.value
    assert data["note"] == "希望します"


# ==================================================
# Get my preferences
# ==================================================
@pytest.mark.asyncio
async def test_get_my_preferences(
    client,
    auth_headers,
    test_slot,
):
    payload = {
        "shift_slot_id": test_slot.id,
        "priority": PreferencePriority.PREFERRED.value,
    }

    await client.post(
        "/shift-preferences",
        headers=auth_headers,
        json=payload,
    )

    res = await client.get(
        f"/shift-preferences/me?shift_slot_id={test_slot.id}",
        headers=auth_headers,
    )

    assert res.status_code == 200

    data = res.json()

    assert isinstance(data, list)
    assert len(data) >= 1


# ==================================================
# Get all
# ==================================================
@pytest.mark.asyncio
async def test_get_all_preferences(
    client,
    auth_headers,
):
    res = await client.get(
        "/shift-preferences",
        headers=auth_headers,
    )

    assert res.status_code == 200

    assert isinstance(res.json(), list)


# ==================================================
# Get by id
# ==================================================
@pytest.mark.asyncio
async def test_get_preference(
    client,
    auth_headers,
    test_slot,
):
    payload = {
        "shift_slot_id": test_slot.id,
        "priority": PreferencePriority.PREFERRED.value,
    }

    created = await client.post(
        "/shift-preferences",
        headers=auth_headers,
        json=payload,
    )

    preference_id = created.json()["id"]

    res = await client.get(
        f"/shift-preferences/{preference_id}",
        headers=auth_headers,
    )

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == preference_id


# ==================================================
# Update
# ==================================================
@pytest.mark.asyncio
async def test_update_preference(
    client,
    auth_headers,
    test_slot,
):
    payload = {
        "shift_slot_id": test_slot.id,
        "priority": PreferencePriority.PREFERRED.value,
    }

    created = await client.post(
        "/shift-preferences",
        headers=auth_headers,
        json=payload,
    )

    preference_id = created.json()["id"]

    res = await client.patch(
        f"/shift-preferences/{preference_id}",
        headers=auth_headers,
        json={
            "priority": PreferencePriority.REQUIRED.value,
            "note": "絶対参加",
        },
    )

    assert res.status_code == 200

    data = res.json()

    assert data["priority"] == PreferencePriority.REQUIRED.value
    assert data["note"] == "絶対参加"


# ==================================================
# Delete
# ==================================================
@pytest.mark.asyncio
async def test_delete_preference(
    client,
    auth_headers,
    test_slot,
):
    payload = {
        "shift_slot_id": test_slot.id,
        "priority": PreferencePriority.PREFERRED.value,
    }

    created = await client.post(
        "/shift-preferences",
        headers=auth_headers,
        json=payload,
    )

    preference_id = created.json()["id"]

    res = await client.delete(
        f"/shift-preferences/{preference_id}",
        headers=auth_headers,
    )

    assert res.status_code == 204


# ==================================================
# Not Found
# ==================================================
@pytest.mark.asyncio
async def test_get_preference_not_found(
    client,
    auth_headers,
):
    res = await client.get(
        "/shift-preferences/999999",
        headers=auth_headers,
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_preference_not_found(
    client,
    auth_headers,
):
    res = await client.patch(
        "/shift-preferences/999999",
        headers=auth_headers,
        json={
            "priority": PreferencePriority.REQUIRED.value,
        },
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_preference_not_found(
    client,
    auth_headers,
):
    res = await client.delete(
        "/shift-preferences/999999",
        headers=auth_headers,
    )

    assert res.status_code == 404