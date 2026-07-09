import pytest


# ==================================================
# シフト生成APIテスト
# ==================================================
@pytest.mark.asyncio
async def test_generate_schedule(client, auth_headers):
    """
    シフトスケジューラが正常に動作することを確認
    """

    res = await client.post(
        "/scheduler/generate",
        headers=auth_headers,
    )
    print(res.text)

    assert res.status_code == 200

    data = res.json()

    # SchedulerResponse形式
    assert isinstance(data, dict)
    assert "message" in data
    assert "assignments" in data
    assert isinstance(data["assignments"], dict)


# ==================================================
# シフト確定APIテスト
# ==================================================
@pytest.mark.asyncio
async def test_confirm_schedule(client, auth_headers):
    """
    シフト確定処理が正常に動作することを確認
    """

    payload = {
        "assignments": {
            "1": [1]
        }
    }

    res = await client.post(
        "/scheduler/confirm",
        headers=auth_headers,
        json=payload,
    )

    print(res.text)

    assert res.status_code == 200

    data = res.json()

    assert isinstance(data, dict)
    assert "message" in data
    assert "assignments" in data


# ==================================================
# スケジュール生成の最低保証テスト
# ==================================================
@pytest.mark.asyncio
async def test_schedule_structure(client, auth_headers):
    """
    レスポンス構造が壊れていないことだけ保証
    """

    res = await client.post(
        "/scheduler/generate",
        headers=auth_headers,
    )

    assert res.status_code == 200

    data = res.json()

    assert isinstance(data, dict)
    assert "assignments" in data

    assignments = data["assignments"]

    # slot -> list[user_id]
    for slot_id, user_ids in assignments.items():
        assert isinstance(slot_id, str) or isinstance(slot_id, int)
        assert isinstance(user_ids, list)