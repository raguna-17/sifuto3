from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.scheduler.algorithm import ShiftSchedulerAlgorithm
from app.domains.shift_assignments.service import ShiftAssignmentService
from app.domains.shift_assignments.model import ShiftAssignment
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.shift_slots.model import ShiftSlot
from app.domains.users.model import User


class SchedulerService:

    @staticmethod
    async def load_data(
        db: AsyncSession,
    ):
        slots = (
            await db.scalars(
                select(ShiftSlot)
            )
        ).all()

        prefs = (
            await db.scalars(
                select(ShiftPreference)
            )
        ).all()

        users = (
            await db.scalars(
                select(User)
            )
        ).all()

        return slots, prefs, users

    @staticmethod
    async def generate(
        db: AsyncSession,
    ):
        slots, prefs, users = await SchedulerService.load_data(db)

        return ShiftSchedulerAlgorithm.generate_schedule(
            slots=slots,
            prefs=prefs,
            users=users,
        )

    @staticmethod
    async def confirm(
        db: AsyncSession,
        assignments: dict[int, list[int]],
    ):

        try:

            # 既存の割り当てを全削除
            await db.execute(
                delete(ShiftAssignment)
            )

            for slot_id, user_ids in assignments.items():

                for user_id in user_ids:

                    await ShiftAssignmentService.create(
                        db=db,
                        user_id=user_id,
                        slot_id=int(slot_id),
                        is_auto=True,
                    )

            await db.commit()

            return assignments

        except Exception:
            await db.rollback()
            raise