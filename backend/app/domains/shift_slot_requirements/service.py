from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.positions.model import Position
from app.domains.shift_slots.model import ShiftSlot

from app.domains.shift_slot_requirements.model import (
    ShiftSlotRequirement,
)


class RequirementNotFoundError(Exception):
    pass


class ShiftSlotNotFoundError(Exception):
    pass


class PositionNotFoundError(Exception):
    pass


class ShiftSlotRequirementService:

    @staticmethod
    async def create(
        db: AsyncSession,
        slot_id: int,
        position_id: int,
        required_count: int,
    ) -> ShiftSlotRequirement:

        slot = await db.get(
            ShiftSlot,
            slot_id,
        )

        if not slot:
            raise ShiftSlotNotFoundError()

        position = await db.get(
            Position,
            position_id,
        )

        if not position:
            raise PositionNotFoundError()

        requirement = ShiftSlotRequirement(
            slot_id=slot_id,
            position_id=position_id,
            required_count=required_count,
        )

        try:
            db.add(requirement)

            await db.commit()
            await db.refresh(
                requirement
            )

            return requirement

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_slot(
        db: AsyncSession,
        slot_id: int,
    ) -> list[ShiftSlotRequirement]:

        result = await db.scalars(
            select(
                ShiftSlotRequirement
            ).where(
                ShiftSlotRequirement.slot_id
                == slot_id
            )
        )

        return list(result)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        requirement_id: int,
    ) -> ShiftSlotRequirement:

        requirement = await db.get(
            ShiftSlotRequirement,
            requirement_id,
        )

        if not requirement:
            raise RequirementNotFoundError()

        return requirement

    @staticmethod
    async def update(
        db: AsyncSession,
        requirement_id: int,
        required_count: int,
    ) -> ShiftSlotRequirement:

        requirement = await (
            ShiftSlotRequirementService
            .get_by_id(
                db=db,
                requirement_id=requirement_id,
            )
        )

        requirement.required_count = (
            required_count
        )

        try:
            await db.commit()
            await db.refresh(
                requirement
            )

            return requirement

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete(
        db: AsyncSession,
        requirement_id: int,
    ) -> None:

        requirement = await (
            ShiftSlotRequirementService
            .get_by_id(
                db=db,
                requirement_id=requirement_id,
            )
        )

        try:
            await db.delete(
                requirement
            )

            await db.commit()

        except Exception:
            await db.rollback()
            raise
