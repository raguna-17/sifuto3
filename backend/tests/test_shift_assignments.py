import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.domains.shift_assignments.service import (
    ShiftAssignmentService,
    DuplicateAssignmentError,
    AssignmentCapacityError,
    UserNotFoundError,
    ShiftSlotNotFoundError,
)

from app.domains.shift_slots.model import ShiftSlot
from app.domains.users.model import User


# =========================
# helper
# =========================
async def create_user(db: AsyncSession):
    user = User(
        name="test",
        email="test@test.com",
        hashed_password="hashed",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_slot(db: AsyncSession, capacity=1):
    slot = ShiftSlot(
        start_at=datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc),
        end_at=datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc),
        required_staff_count=capacity,
    )
    db.add(slot)
    await db.commit()
    await db.refresh(slot)
    return slot


# =========================
# tests
# =========================
@pytest.mark.asyncio
async def test_create_assignment_success(db_session: AsyncSession):

    user = await create_user(db_session)
    slot = await create_slot(db_session)

    result = await ShiftAssignmentService.create(
        db=db_session,
        user_id=user.id,
        slot_id=slot.id,
    )

    assert result.id is not None
    assert result.user_id == user.id
    assert result.slot_id == slot.id


@pytest.mark.asyncio
async def test_duplicate_assignment_error(db_session: AsyncSession):

    user = await create_user(db_session)
    slot = await create_slot(db_session)

    await ShiftAssignmentService.create(db_session, user.id, slot.id)

    with pytest.raises(DuplicateAssignmentError):
        await ShiftAssignmentService.create(db_session, user.id, slot.id)


@pytest.mark.asyncio
async def test_user_not_found(db_session: AsyncSession):

    slot = await create_slot(db_session)

    with pytest.raises(UserNotFoundError):
        await ShiftAssignmentService.create(
            db=db_session,
            user_id=9999,
            slot_id=slot.id,
        )


@pytest.mark.asyncio
async def test_slot_not_found(db_session: AsyncSession):

    user = await create_user(db_session)

    with pytest.raises(ShiftSlotNotFoundError):
        await ShiftAssignmentService.create(
            db=db_session,
            user_id=user.id,
            slot_id=9999,
        )


@pytest.mark.asyncio
async def test_capacity_limit(db_session: AsyncSession):

    user1 = await create_user(db_session)
    user2 = await create_user(db_session)

    slot = await create_slot(db_session, capacity=1)

    await ShiftAssignmentService.create(db_session, user1.id, slot.id)

    with pytest.raises(AssignmentCapacityError):
        await ShiftAssignmentService.create(db_session, user2.id, slot.id)