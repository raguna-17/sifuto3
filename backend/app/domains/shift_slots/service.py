from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_slots.schema import (
    ShiftSlotCreate,
    ShiftSlotUpdate,
)


class ShiftSlotNotFoundError(Exception):
    pass


class InvalidShiftTimeError(Exception):
    pass


class ShiftSlotService:

    @staticmethod
    async def create(
        db: AsyncSession,
        slot_in: ShiftSlotCreate,
    ) -> ShiftSlot:

        if slot_in.start_at >= slot_in.end_at:
            raise InvalidShiftTimeError()

        slot = ShiftSlot(
            target_date=slot_in.target_date,
            start_at=slot_in.start_at,
            end_at=slot_in.end_at,
        )

        try:
            db.add(slot)

            await db.commit()
            await db.refresh(slot)

            return slot

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[ShiftSlot]:

        result = await db.scalars(
            select(ShiftSlot)
        )

        return list(result)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        slot_id: int,
    ) -> ShiftSlot:

        slot = await db.get(
            ShiftSlot,
            slot_id,
        )

        if not slot:
            raise ShiftSlotNotFoundError()

        return slot

    @staticmethod
    async def update(
        db: AsyncSession,
        slot_id: int,
        slot_in: ShiftSlotUpdate,
    ) -> ShiftSlot:

        slot = await ShiftSlotService.get_by_id(
            db=db,
            slot_id=slot_id,
        )

        update_data = slot_in.model_dump(
            exclude_unset=True
        )

        new_start = update_data.get(
            "start_at",
            slot.start_at,
        )

        new_end = update_data.get(
            "end_at",
            slot.end_at,
        )

        if new_start >= new_end:
            raise InvalidShiftTimeError()

        for field, value in update_data.items():
            setattr(slot, field, value)

        try:
            await db.commit()
            await db.refresh(slot)

            return slot

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete(
        db: AsyncSession,
        slot_id: int,
    ) -> None:

        slot = await ShiftSlotService.get_by_id(
            db=db,
            slot_id=slot_id,
        )

        try:
            await db.delete(slot)
            await db.commit()

        except Exception:
            await db.rollback()
            raise

