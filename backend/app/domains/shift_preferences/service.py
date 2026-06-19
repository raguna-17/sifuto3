from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.model import User
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.shift_preferences.schema import (
    ShiftPreferenceCreate,
    ShiftPreferenceUpdate,
)


# ==========================================
# Exceptions
# ==========================================

class ShiftPreferenceNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class ShiftPreferenceConflictError(Exception):
    pass


# ==========================================
# Service
# ==========================================
class ShiftPreferenceService:

    # ------------------------------------------
    # create
    # ------------------------------------------
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        preference_in: ShiftPreferenceCreate,
    ) -> ShiftPreference:

        # ユーザー存在チェック
        user = await db.get(User, user_id)
        if user is None:
            raise UserNotFoundError()

        # 重複チェック（ここが今回の本体）
        existing = await db.scalar(
            select(ShiftPreference).where(
                ShiftPreference.user_id == user_id,
                ShiftPreference.shift_slot_id == preference_in.shift_slot_id,
            )
        )

        if existing:
            raise ShiftPreferenceConflictError(
                "shift preference already exists for this user and slot"
            )

        preference = ShiftPreference(
            user_id=user_id,
            shift_slot_id=preference_in.shift_slot_id,
            priority=preference_in.priority,
            note=preference_in.note,
        )

        try:
            db.add(preference)
            await db.commit()
            await db.refresh(preference)
            return preference

        except Exception:
            await db.rollback()
            raise


    # ------------------------------------------
    # get all
    # ------------------------------------------
    @staticmethod
    async def get_all(db: AsyncSession) -> list[ShiftPreference]:

        result = await db.scalars(select(ShiftPreference))
        return list(result)


    # ------------------------------------------
    # get by id
    # ------------------------------------------
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        preference_id: int,
    ) -> ShiftPreference:

        preference = await db.get(ShiftPreference, preference_id)

        if preference is None:
            raise ShiftPreferenceNotFoundError()

        return preference


    # ------------------------------------------
    # get by user
    # ------------------------------------------
    @staticmethod
    async def get_by_user(
        db: AsyncSession,
        user_id: int,
    ) -> list[ShiftPreference]:

        result = await db.scalars(
            select(ShiftPreference).where(
                ShiftPreference.user_id == user_id
            )
        )

        return list(result)


    # ------------------------------------------
    # update
    # ------------------------------------------
    @staticmethod
    async def update(
        db: AsyncSession,
        preference_id: int,
        preference_in: ShiftPreferenceUpdate,
    ) -> ShiftPreference:

        preference = await ShiftPreferenceService.get_by_id(
            db=db,
            preference_id=preference_id,
        )

        update_data = preference_in.model_dump(exclude_unset=True)

        # 更新後の重複チェック（地味に重要）
        new_slot_id = update_data.get("shift_slot_id", preference.shift_slot_id)
        new_user_id = preference.user_id

        existing = await db.scalar(
            select(ShiftPreference).where(
                ShiftPreference.user_id == new_user_id,
                ShiftPreference.shift_slot_id == new_slot_id,
                ShiftPreference.id != preference_id,
            )
        )

        if existing:
            raise ShiftPreferenceConflictError(
                "duplicate preference after update"
            )

        for field, value in update_data.items():
            setattr(preference, field, value)

        try:
            await db.commit()
            await db.refresh(preference)
            return preference

        except Exception:
            await db.rollback()
            raise


    # ------------------------------------------
    # delete
    # ------------------------------------------
    @staticmethod
    async def delete(
        db: AsyncSession,
        preference_id: int,
    ) -> None:

        preference = await ShiftPreferenceService.get_by_id(
            db=db,
            preference_id=preference_id,
        )

        try:
            await db.delete(preference)
            await db.commit()

        except Exception:
            await db.rollback()
            raise