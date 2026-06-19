from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.domains.users.model import User
from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_assignments.model import ShiftAssignment


# =========================
# Exceptions
# =========================
class ShiftAssignmentNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class ShiftSlotNotFoundError(Exception):
    pass


class AssignmentCapacityError(Exception):
    pass


class DuplicateAssignmentError(Exception):
    pass


# =========================
# Service
# =========================
class ShiftAssignmentService:

    # =========================
    # create
    # =========================
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        slot_id: int,
        is_auto: bool = True,
    ) -> ShiftAssignment:

        user = await db.get(User, user_id)
        if user is None:
            raise UserNotFoundError()

        slot = await db.get(ShiftSlot, slot_id)
        if slot is None:
            raise ShiftSlotNotFoundError()

        # =========================
        # 1. 重複チェック（軽く残す）
        # =========================
        existing = await db.scalar(
            select(ShiftAssignment).where(
                ShiftAssignment.user_id == user_id,
                ShiftAssignment.slot_id == slot_id,
            )
        )
        if existing:
            raise DuplicateAssignmentError()

        assignment = ShiftAssignment(
            user_id=user_id,
            slot_id=slot_id,
            is_auto=is_auto,
            is_confirmed=False,
        )

        try:
            db.add(assignment)
            await db.flush()  # ←重要（ここでDB制約チェックさせる）

            # =========================
            # 2. capacityチェックは「再計算」する
            # =========================
            current_count = await db.scalar(
                select(func.count(ShiftAssignment.id)).where(
                    ShiftAssignment.slot_id == slot_id
                )
            ) or 0

            if current_count > slot.required_staff_count:
                await db.rollback()
                raise AssignmentCapacityError()

            await db.commit()
            await db.refresh(assignment)
            return assignment

        except IntegrityError:
            await db.rollback()
            raise DuplicateAssignmentError()

        except Exception:
            await db.rollback()
            raise

    # =========================
    # get all
    # =========================
    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[ShiftAssignment]:

        result = await db.scalars(select(ShiftAssignment))
        return result.all()

    # =========================
    # get by id
    # =========================
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        assignment_id: int,
    ) -> ShiftAssignment:

        assignment = await db.get(ShiftAssignment, assignment_id)

        if assignment is None:
            raise ShiftAssignmentNotFoundError()

        return assignment

    # =========================
    # get by user
    # =========================
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
        return result.all()

    # =========================
    # get by slot
    # =========================
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
        return result.all()

    # =========================
    # update
    # =========================
    @staticmethod
    async def update(
        db: AsyncSession,
        assignment_id: int,
        assignment_in,
    ) -> ShiftAssignment:

        assignment = await ShiftAssignmentService.get_by_id(
            db=db,
            assignment_id=assignment_id,
        )

        update_data = assignment_in.model_dump(exclude_unset=True)

        # adminが確定するケース想定
        if "is_confirmed" in update_data:
            assignment.is_confirmed = update_data["is_confirmed"]

        try:
            await db.commit()
            await db.refresh(assignment)
            return assignment

        except Exception:
            await db.rollback()
            raise

    # =========================
    # delete
    # =========================
    @staticmethod
    async def delete(
        db: AsyncSession,
        assignment_id: int,
    ) -> None:

        assignment = await ShiftAssignmentService.get_by_id(
            db=db,
            assignment_id=assignment_id,
        )

        try:
            await db.delete(assignment)
            await db.commit()

        except Exception:
            await db.rollback()
            raise