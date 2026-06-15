from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.shift_slots.model import ShiftSlot
from app.domains.shift_slots.schema import (
    ShiftSlotCreate,
    ShiftSlotUpdate,
)


# ==========================================
# Exceptions
# ==========================================

class ShiftSlotNotFoundError(Exception):
    pass


class ShiftSlotConflictError(Exception):
    pass


class ShiftSlotInPastError(Exception):
    pass


class ShiftSlotService:

    # ==========================================
    # 共通バリデーション（業務ルール）
    # ==========================================
    @staticmethod
    def _validate_business_rules(
        *,
        start_at: datetime,
        end_at: datetime,
        required_position,
    ) -> None:

        now = datetime.now(timezone.utc)

        # 過去チェック（業務ルール）
        if start_at < now:
            raise ShiftSlotInPastError("cannot create past shift slot")

        # 募集期間が長すぎる制限（任意の業務ルール）
        duration = end_at - start_at

        if duration.total_seconds() > 86400:
            raise ValueError("shift slot cannot exceed 24 hours")

        # 将来拡張：ポジション制約チェックなど
        if required_position is None:
            raise ValueError("required_position is required")


    # ==========================================
    # Create
    # ==========================================
    @staticmethod
    async def create(
        db: AsyncSession,
        slot_in: ShiftSlotCreate,
    ) -> ShiftSlot:

        ShiftSlotService._validate_business_rules(
            start_at=slot_in.start_at,
            end_at=slot_in.end_at,
            required_position=slot_in.required_position,
        )

        # 重複チェック（業務ロジック）
        conflict = await db.scalar(
            select(ShiftSlot).where(
                ShiftSlot.start_at == slot_in.start_at,
                ShiftSlot.end_at == slot_in.end_at,
                ShiftSlot.required_position == slot_in.required_position,
            )
        )

        if conflict:
            raise ShiftSlotConflictError("shift slot already exists")

        slot = ShiftSlot(
            start_at=slot_in.start_at,
            end_at=slot_in.end_at,
            required_staff_count=slot_in.required_staff_count,
            required_position=slot_in.required_position,
        )

        try:
            db.add(slot)
            await db.commit()
            await db.refresh(slot)
            return slot

        except Exception:
            await db.rollback()
            raise


    # ==========================================
    # Get all
    # ==========================================
    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[ShiftSlot]:

        result = await db.scalars(
            select(ShiftSlot)
            .order_by(ShiftSlot.start_at)
        )

        return list(result)


    # ==========================================
    # Get by id
    # ==========================================
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        slot_id: int,
    ) -> ShiftSlot:

        slot = await db.get(ShiftSlot, slot_id)

        if slot is None:
            raise ShiftSlotNotFoundError()

        return slot


    # ==========================================
    # Update
    # ==========================================
    @staticmethod
    async def update(
        db: AsyncSession,
        slot_id: int,
        slot_in: ShiftSlotUpdate,
    ) -> ShiftSlot:

        slot = await ShiftSlotService.get_by_id(db, slot_id)

        update_data = slot_in.model_dump(exclude_unset=True)

        new_start = update_data.get("start_at", slot.start_at)
        new_end = update_data.get("end_at", slot.end_at)
        new_position = update_data.get("required_position", slot.required_position)

        # 業務ルールチェック
        ShiftSlotService._validate_business_rules(
            start_at=new_start,
            end_at=new_end,
            required_position=new_position,
        )

        # 更新
        for field, value in update_data.items():
            setattr(slot, field, value)

        try:
            await db.commit()
            await db.refresh(slot)
            return slot

        except Exception:
            await db.rollback()
            raise


    # ==========================================
    # Delete
    # ==========================================
    @staticmethod
    async def delete(
        db: AsyncSession,
        slot_id: int,
    ) -> None:

        slot = await ShiftSlotService.get_by_id(db, slot_id)

        try:
            await db.delete(slot)
            await db.commit()

        except Exception:
            await db.rollback()
            raise