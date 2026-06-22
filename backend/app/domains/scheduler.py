import logging
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.dependencies import AdminUser
from app.core.enums import PreferencePriority

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User
from app.domains.shift_assignments.service import ShiftAssignmentService


router = APIRouter(prefix="/scheduler", tags=["scheduler"])
logger = logging.getLogger(__name__)


# ==================================================
# scheduler logic (全部ここ)
# ==================================================
class ShiftScheduler:

    @staticmethod
    def generate_schedule(
        slots: list[ShiftSlot],
        prefs: list[ShiftPreference],
        users: list[User],
    ) -> dict[int, list[int]]:

        logger.info("schedule generation started")

        result: dict[int, list[int]] = defaultdict(list)
        slot_counts: dict[int, int] = defaultdict(int)
        user_prefs: dict[int, list[ShiftPreference]] = defaultdict(list)

        for pref in prefs:
            user_prefs[pref.user_id].append(pref)

        for slot in slots:

            candidates: list[tuple[int, int]] = []

            for user in users:

                prefs_for_user = user_prefs.get(user.id, [])

                score = ShiftScheduler._calculate_score(
                    slot=slot,
                    prefs=prefs_for_user,
                )

                if score > 0:
                    candidates.append((user.id, score))

            candidates.sort(key=lambda x: x[1], reverse=True)

            for user_id, _ in candidates:

                if slot_counts[slot.id] >= slot.required_staff_count:
                    break

                if user_id in result[slot.id]:
                    continue

                result[slot.id].append(user_id)
                slot_counts[slot.id] += 1

        logger.info(
            "schedule generation completed",
            extra={
                "slot_count": len(slots),
                "assignment_total": sum(len(v) for v in result.values()),
            },
        )

        return dict(result)

    @staticmethod
    def _calculate_score(
        slot: ShiftSlot,
        prefs: list[ShiftPreference],
    ) -> int:

        target_pref = next(
            (p for p in prefs if p.shift_slot_id == slot.id),
            None,
        )

        if target_pref is None:
            return 0

        if target_pref.priority == PreferencePriority.UNAVAILABLE:
            return -999

        if target_pref.priority == PreferencePriority.REQUIRED:
            return 100

        if target_pref.priority == PreferencePriority.PREFERRED:
            return 10

        if target_pref.priority == PreferencePriority.NEUTRAL:
            return 1

        if target_pref.priority == PreferencePriority.AVOID:
            return -20

        return 0


# ==================================================
# DB loading (ここも統合)
# ==================================================
async def load_scheduler_data(db: AsyncSession):
    slots = (await db.scalars(select(ShiftSlot))).all()
    prefs = (await db.scalars(select(ShiftPreference))).all()
    users = (await db.scalars(select(User))).all()

    return slots, prefs, users


# ==================================================
# API
# ==================================================
@router.post("/generate")
async def generate_schedule(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):

    slots, prefs, users = await load_scheduler_data(db)

    result = ShiftScheduler.generate_schedule(
        slots=slots,
        prefs=prefs,
        users=users,
    )

    return {
        "message": "schedule generated",
        "assignments": result,
    }


@router.post("/confirm")
async def confirm_schedule(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):

    slots, prefs, users = await load_scheduler_data(db)

    result = ShiftScheduler.generate_schedule(
        slots=slots,
        prefs=prefs,
        users=users,
    )

    for slot_id, user_ids in result.items():
        for user_id in user_ids:
            await ShiftAssignmentService.create(
                db=db,
                user_id=user_id,
                slot_id=slot_id,
                is_auto=True,
            )

    return {"status": "ok"}