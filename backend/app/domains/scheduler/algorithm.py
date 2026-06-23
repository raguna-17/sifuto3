import logging
from collections import defaultdict
from datetime import timedelta

from app.core.enums import PreferencePriority
from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User


logger = logging.getLogger(__name__)


class ShiftSchedulerAlgorithm:

    @staticmethod
    def generate_schedule(
        slots: list[ShiftSlot],
        prefs: list[ShiftPreference],
        users: list[User],
    ) -> dict[int, list[int]]:

        logger.info("schedule generation started")

        result: dict[int, list[int]] = defaultdict(list)
        slot_counts: dict[int, int] = defaultdict(int)

        # 公平性用
        user_work_count: dict[int, int] = defaultdict(int)

        # userごとにprefまとめる
        user_prefs: dict[int, list[ShiftPreference]] = defaultdict(list)
        for pref in prefs:
            user_prefs[pref.user_id].append(pref)

        # slotは時間順（重要）
        slots = sorted(slots, key=lambda s: s.start_at)

        for slot in slots:

            candidates: list[tuple[int, int]] = []

            for user in users:

                score = ShiftSchedulerAlgorithm._calculate_score(
                    slot=slot,
                    prefs=user_prefs.get(user.id, []),
                    user_work_count=user_work_count[user.id],
                )

                if score <= 0:
                    continue

                candidates.append((user.id, score))

            # スコア降順
            candidates.sort(key=lambda x: x[1], reverse=True)

            for user_id, _ in candidates:

                if slot_counts[slot.id] >= slot.required_staff_count:
                    break

                if user_id in result[slot.id]:
                    continue

                result[slot.id].append(user_id)
                slot_counts[slot.id] += 1
                user_work_count[user_id] += 1

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
        user_work_count: int,
    ) -> int:

        score = 0

        # -------------------------
        # preference score
        # -------------------------
        target_pref = next(
            (p for p in prefs if p.shift_slot_id == slot.id),
            None,
        )

        if target_pref is None:
            score += 0
        else:
            if target_pref.priority == PreferencePriority.UNAVAILABLE:
                return -999

            if target_pref.priority == PreferencePriority.REQUIRED:
                score += 100

            elif target_pref.priority == PreferencePriority.PREFERRED:
                score += 20

            elif target_pref.priority == PreferencePriority.NEUTRAL:
                score += 5

            elif target_pref.priority == PreferencePriority.AVOID:
                score -= 30

        # -------------------------
        # fairness penalty
        # -------------------------
        score -= user_work_count * 3

        return score