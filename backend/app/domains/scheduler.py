from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.users.model import User
from app.domains.shift_assignments.model import ShiftAssignment
from app.core.enums import PreferencePriority


class ShiftScheduler:

    # =========================================
    # main entry point
    # =========================================
    @staticmethod
    async def generate_schedule(
        db: AsyncSession,
    ) -> dict[int, list[int]]:
        """
        return:
            {
                slot_id: [user_id, user_id...]
            }
        """

        slots = (await db.scalars(select(ShiftSlot))).all()
        prefs = (await db.scalars(select(ShiftPreference))).all()
        users = (await db.scalars(select(User))).all()

        # slot_id -> assigned users
        result: dict[int, list[int]] = defaultdict(list)

        # userごとの希望をまとめる
        user_prefs: dict[int, list[ShiftPreference]] = defaultdict(list)
        for p in prefs:
            user_prefs[p.user_id].append(p)

        # slotごとの現在人数
        slot_counts: dict[int, int] = defaultdict(int)

        # =========================================
        # greedy assignment
        # =========================================
        for slot in slots:

            # slotごとの候補ユーザー
            candidates = []

            for user in users:
                prefs_for_user = user_prefs.get(user.id, [])

                score = self._calculate_score(
                    slot=slot,
                    prefs=prefs_for_user,
                )

                if score > 0:
                    candidates.append((user.id, score))

            # スコア順
            candidates.sort(key=lambda x: x[1], reverse=True)

            # 定員まで詰める
            for user_id, _ in candidates:
                if slot_counts[slot.id] >= slot.required_staff_count:
                    break

                if user_id in result[slot.id]:
                    continue

                result[slot.id].append(user_id)
                slot_counts[slot.id] += 1

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

            # 日付一致
            if p.target_date != slot.start_at.date():
                continue

            # 時間制約チェック
            if p.start_at and p.end_at:
                if slot.start_at >= p.end_at or slot.end_at <= p.start_at:
                    continue

            # priority加点
            if p.priority == PreferencePriority.REQUIRED:
                score += 100
            elif p.priority == PreferencePriority.PREFERRED:
                score += 10
            elif p.priority == PreferencePriority.NEUTRAL:
                score += 1
            elif p.priority == PreferencePriority.AVOID:
                score -= 20
            elif p.priority == PreferencePriority.UNAVAILABLE:
                score -= 999

        return score