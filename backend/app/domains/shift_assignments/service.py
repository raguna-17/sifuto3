from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.model import User
from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_assignments.model import (
    ShiftAssignment,
)

from app.domains.shift_assignments.schema import (
    ShiftAssignmentCreate,
    ShiftAssignmentUpdate,
)


class ShiftAssignmentNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class ShiftSlotNotFoundError(Exception):
    pass


class ShiftAssignmentService:

    @staticmethod
    async def create(
        db: AsyncSession,
        assignment_in: ShiftAssignmentCreate,
    ) -> ShiftAssignment:

        user = await db.get(
            User,
            assignment_in.user_id,
        )

        if not user:
            raise UserNotFoundError()

        slot = await db.get(
            ShiftSlot,
            assignment_in.slot_id,
        )

        if not slot:
            raise ShiftSlotNotFoundError()

        assignment = ShiftAssignment(
            user_id=assignment_in.user_id,
            slot_id=assignment_in.slot_id,
            is_auto=assignment_in.is_auto,
        )

        try:
            db.add(assignment)

            await db.commit()
            await db.refresh(
                assignment
            )

            return assignment

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[ShiftAssignment]:

        result = await db.scalars(
            select(ShiftAssignment)
        )

        return list(result)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        assignment_id: int,
    ) -> ShiftAssignment:

        assignment = await db.get(
            ShiftAssignment,
            assignment_id,
        )

        if not assignment:
            raise ShiftAssignmentNotFoundError()

        return assignment

    @staticmethod
    async def get_by_user(
        db: AsyncSession,
        user_id: int,
    ) -> list[ShiftAssignment]:

        result = await db.scalars(
            select(ShiftAssignment).where(
                ShiftAssignment.user_id == user_id
            )
        )

        return list(result)

    @staticmethod
    async def get_by_slot(
        db: AsyncSession,
        slot_id: int,
    ) -> list[ShiftAssignment]:

        result = await db.scalars(
            select(ShiftAssignment).where(
                ShiftAssignment.slot_id == slot_id
            )
        )

        return list(result)

    @staticmethod
    async def update(
        db: AsyncSession,
        assignment_id: int,
        assignment_in: ShiftAssignmentUpdate,
    ) -> ShiftAssignment:

        assignment = await (
            ShiftAssignmentService.get_by_id(
                db=db,
                assignment_id=assignment_id,
            )
        )

        update_data = (
            assignment_in.model_dump(
                exclude_unset=True,
            )
        )

        for field, value in update_data.items():
            setattr(
                assignment,
                field,
                value,
            )

        try:
            await db.commit()

            await db.refresh(
                assignment
            )

            return assignment

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete(
        db: AsyncSession,
        assignment_id: int,
    ) -> None:

        assignment = await (
            ShiftAssignmentService.get_by_id(
                db=db,
                assignment_id=assignment_id,
            )
        )

        try:
            await db.delete(
                assignment
            )

            await db.commit()

        except Exception:
            await db.rollback()
            raise
