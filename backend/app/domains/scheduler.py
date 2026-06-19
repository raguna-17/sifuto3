import logging
from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User
from app.core.enums import PreferencePriority

logger = logging.getLogger(__name__)


class ShiftScheduler:

    # =========================================
    # main entry point
    # =========================================
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
        for p in prefs:
            user_prefs[p.user_id].append(p)

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

            logger.info(
                "slot evaluated",
                extra={
                    "slot_id": slot.id,
                    "candidate_count": len(candidates),
                    "required_staff": slot.required_staff_count,
                },
            )

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

        return result

    # =========================================
    # scoring logic
    # =========================================
    @staticmethod
    def _calculate_score(
        slot: ShiftSlot,
        prefs: list[ShiftPreference],
    ) -> int:

        score = 0

        for p in prefs:

            if p.priority == PreferencePriority.UNAVAILABLE:
                logger.debug(
                    "user excluded by preference",
                    extra={
                        "user_id": p.user_id,
                        "slot_id": slot.id,
                        "priority": p.priority.value,
                    },
                )
                return -999

            if p.priority == PreferencePriority.REQUIRED:
                score += 100

            elif p.priority == PreferencePriority.PREFERRED:
                score += 10

            elif p.priority == PreferencePriority.NEUTRAL:
                score += 1

            elif p.priority == PreferencePriority.AVOID:
                score -= 20

        return score