from collections import defaultdict
import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User

from app.core.enums import PreferencePriority
from app.core.dependencies import AdminUser

logger = logging.getLogger(__name__)

router = APIRouter(
prefix="/scheduler",
tags=["scheduler"],
)

class ShiftScheduler:


    @staticmethod
    async def generate_schedule(
        db: AsyncSession,
    ) -> dict[int, list[int]]:

        logger.info("schedule generation started")

        slots = (await db.scalars(select(ShiftSlot))).all()
        prefs = (await db.scalars(select(ShiftPreference))).all()
        users = (await db.scalars(select(User))).all()

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
                    candidates.append(
                        (
                            user.id,
                            score,
                        )
                    )

            candidates.sort(
                key=lambda x: x[1],
                reverse=True,
            )

            logger.info(
                "slot evaluated",
                extra={
                    "slot_id": slot.id,
                    "candidate_count": len(candidates),
                    "required_staff": slot.required_staff_count,
                },
            )

            for user_id, _ in candidates:

                if (
                    slot_counts[slot.id]
                    >= slot.required_staff_count
                ):
                    break

                if user_id in result[slot.id]:
                    continue

                result[slot.id].append(user_id)
                slot_counts[slot.id] += 1

        logger.info(
            "schedule generation completed",
            extra={
                "slot_count": len(slots),
                "assignment_total": sum(
                    len(v) for v in result.values()
                ),
            },
        )

        return dict(result)

    @staticmethod
    def _calculate_score(
        slot: ShiftSlot,
        prefs: list[ShiftPreference],
    ) -> int:

        target_pref = next(
            (
                p
                for p in prefs
                if p.shift_slot_id == slot.id
            ),
            None,
        )

        if target_pref is None:
            return 0

        if (
            target_pref.priority
            == PreferencePriority.UNAVAILABLE
        ):
            return -999

        if (
            target_pref.priority
            == PreferencePriority.REQUIRED
        ):
            return 100

        if (
            target_pref.priority
            == PreferencePriority.PREFERRED
        ):
            return 10

        if (
            target_pref.priority
            == PreferencePriority.NEUTRAL
        ):
            return 1

        if (
            target_pref.priority
            == PreferencePriority.AVOID
        ):
            return -20

        return 0


@router.post("/generate")
async def generate_schedule(
_: AdminUser,
db: AsyncSession = Depends(get_db),
):
    result = await ShiftScheduler.generate_schedule(db)


    return {
        "message": "schedule generated",
        "assignments": result,
    }

@router.post("/confirm")
async def confirm_schedule(
    _: AdminUser,
    db: AsyncSession = Depends(get_db),
):
    result = await ShiftScheduler.generate_schedule(db)

    # ここでDB保存
    for slot_id, user_ids in result.items():
        for user_id in user_ids:
            await ShiftAssignmentService.create(
                db=db,
                user_id=user_id,
                slot_id=slot_id,
                is_auto=True,
            )

    return {"status": "ok"}

