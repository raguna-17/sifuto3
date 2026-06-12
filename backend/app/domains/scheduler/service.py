from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_slot_requirements.model import ShiftSlotRequirement
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.shift_assignments.model import ShiftAssignment
from app.core.enums import PreferencePriority


class SchedulerService:

    @staticmethod
    async def run(
        db: AsyncSession,
    ) -> list[ShiftAssignment]:

        slots = (
            await db.scalars(
                select(ShiftSlot)
            )
        ).all()

        created_assignments = []

        for slot in slots:

            # =========================
            # 1. 蠢・ｦ∽ｺｺ謨ｰ蜿門ｾ・
            # =========================
            requirements = await db.scalars(
                select(ShiftSlotRequirement).where(
                    ShiftSlotRequirement.slot_id == slot.id
                )
            )
            requirements = list(requirements)

            # =========================
            # 2. 蟶梧悍荳隕ｧ蜿門ｾ・
            # =========================
            preferences = await db.scalars(
                select(ShiftPreference).where(
                    ShiftPreference.target_date == slot.target_date
                )
            )
            preferences = list(preferences)

            # =========================
            # 3. 蜆ｪ蜈亥ｺｦ繧ｽ繝ｼ繝・
            # =========================
            def priority_value(p: ShiftPreference):
                return {
                    PreferencePriority.REQUIRED: 0,
                    PreferencePriority.PREFERRED: 1,
                    PreferencePriority.NEUTRAL: 2,
                    PreferencePriority.AVOID: 3,
                    PreferencePriority.UNAVAILABLE: 999,
                }[p.priority]

            preferences.sort(key=priority_value)

            # =========================
            # 4. 蜑ｲ蠖灘・逅・
            # =========================
            for req in requirements:

                assigned_count = 0

                for pref in preferences:

                    if assigned_count >= req.required_count:
                        break

                    if pref.priority == PreferencePriority.UNAVAILABLE:
                        continue

                    if pref.priority == PreferencePriority.AVOID:
                        continue

                    # 譌｢縺ｫ蜷茎lot縺ｧ蜑ｲ蠖捺ｸ医∩縺ｪ繧峨せ繧ｭ繝・・
                    exists = await db.scalar(
                        select(ShiftAssignment).where(
                            ShiftAssignment.slot_id == slot.id,
                            ShiftAssignment.user_id == pref.user_id,
                        )
                    )

                    if exists:
                        continue

                    assignment = ShiftAssignment(
                        user_id=pref.user_id,
                        slot_id=slot.id,
                        is_auto=True,
                        status="confirmed",
                    )

                    db.add(assignment)
                    created_assignments.append(assignment)

                    assigned_count += 1

        await db.commit()

        for a in created_assignments:
            await db.refresh(a)

        return created_assignments
