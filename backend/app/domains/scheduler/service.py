from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User
from app.domains.shift_assignments.service import ShiftAssignmentService

from .algorithm import ShiftSchedulerAlgorithm


class SchedulerService:

    @staticmethod
    async def load_data(db: AsyncSession):
        slots = (await db.scalars(select(ShiftSlot))).all()
        prefs = (await db.scalars(select(ShiftPreference))).all()
        users = (await db.scalars(select(User))).all()
        return slots, prefs, users

    @staticmethod
    async def generate(db: AsyncSession):

        slots, prefs, users = await SchedulerService.load_data(db)

        return ShiftSchedulerAlgorithm.generate_schedule(
            slots=slots,
            prefs=prefs,
            users=users,
        )

    @staticmethod
    async def confirm(db: AsyncSession):

        result = await SchedulerService.generate(db)

        # ここも軽く安全化
        for slot_id, user_ids in result.items():
            for user_id in user_ids:
                await ShiftAssignmentService.create(
                    db=db,
                    user_id=user_id,
                    slot_id=slot_id,
                    is_auto=True,
                )

        return result