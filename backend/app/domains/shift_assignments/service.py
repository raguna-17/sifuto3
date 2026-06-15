from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.model import User
from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_assignments.model import ShiftAssignment
from app.core.enums import ShiftStatus
from sqlalchemy.exc import IntegrityError


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


class InvalidStatusTransitionError(Exception):
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
        assignment_in,
    ) -> ShiftAssignment:

        # -------------------------
        # user check
        # -------------------------
        user = await db.get(User, assignment_in.user_id)
        if user is None:
            raise UserNotFoundError()

        # -------------------------
        # slot check
        # -------------------------
        slot = await db.get(ShiftSlot, assignment_in.slot_id)
        if slot is None:
            raise ShiftSlotNotFoundError()

        # -------------------------
        # duplicate check（アプリ側ガード）
        # -------------------------
        existing = await db.scalar(
            select(ShiftAssignment).where(
                ShiftAssignment.user_id == assignment_in.user_id,
                ShiftAssignment.slot_id == assignment_in.slot_id,
            )
        )
        if existing:
            raise DuplicateAssignmentError()

        # -------------------------
        # capacity check（最新状態保証）
        # -------------------------
        current_count = await db.scalar(
            select(func.count(ShiftAssignment.id)).where(
                ShiftAssignment.slot_id == assignment_in.slot_id
            )
        )

        if current_count >= slot.required_staff_count:
            raise AssignmentCapacityError()

        # -------------------------
        # create entity
        # -------------------------
        assignment = ShiftAssignment(
            user_id=assignment_in.user_id,
            slot_id=assignment_in.slot_id,
            is_auto=assignment_in.is_auto,
            status=ShiftStatus.CONFIRMED,
        )

        try:
            db.add(assignment)
            await db.commit()
            await db.refresh(assignment)
            return assignment

        except IntegrityError:
            # DB側のユニーク制約に引っかかった場合
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

        result = await db.scalars(
            select(ShiftAssignment)
        )
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

        # -------------------------
        # status transition guard
        # -------------------------
        if "status" in update_data:
            new_status = update_data["status"]

            if assignment.status == ShiftStatus.CANCELED:
                raise InvalidStatusTransitionError("already canceled")

            # 最低限：同値更新禁止
            if assignment.status == new_status:
                pass

        for field, value in update_data.items():
            setattr(assignment, field, value)

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