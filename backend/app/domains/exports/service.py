from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_assignments.model import ShiftAssignment
from app.domains.shift_slots.model import ShiftSlot
from app.domains.users.model import User
from app.domains.exports.schema import ShiftExportRow


class ShiftExportService:

    @staticmethod
    async def build_export_rows(db: AsyncSession) -> list[ShiftExportRow]:
        """
        シフト出力用データを生成する（Async版）
        """

        # -------------------------
        # assignments
        # -------------------------
        result = await db.scalars(select(ShiftAssignment))
        assignments = result.all()

        if not assignments:
            return []

        slot_ids = {a.slot_id for a in assignments}
        user_ids = {a.user_id for a in assignments}

        # -------------------------
        # slots
        # -------------------------
        slot_result = await db.scalars(
            select(ShiftSlot).where(ShiftSlot.id.in_(slot_ids))
        )
        slots = slot_result.all()

        # -------------------------
        # users
        # -------------------------
        user_result = await db.scalars(
            select(User).where(User.id.in_(user_ids))
        )
        users = user_result.all()

        # -------------------------
        # mapping
        # -------------------------
        slot_map = {s.id: s for s in slots}
        user_map = {u.id: u for u in users}

        # -------------------------
        # build rows
        # -------------------------
        rows: list[ShiftExportRow] = []

        for a in assignments:
            slot = slot_map.get(a.slot_id)
            user = user_map.get(a.user_id)

            if not slot or not user:
                continue

            rows.append(
                ShiftExportRow(
                    date=slot.start_at.date().isoformat(),
                    slot_id=slot.id,
                    user_id=user.id,
                    user_name=user.name,
                    is_auto=a.is_auto,
                    is_confirmed=a.is_confirmed,
                    required_staff_count=slot.required_staff_count,
                )
            )

        return rows