from datetime import datetime

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


class InvalidPreferenceTimeError(Exception):
    pass


# ==========================================
# Service
# ==========================================
class ShiftPreferenceService:

    # ------------------------------------------
    # 共通バリデーション
    # ------------------------------------------
    @staticmethod
    def _validate_time_range(
        start_at: datetime | None,
        end_at: datetime | None,
    ) -> None:

        # 片方だけNG
        if (start_at is None) != (end_at is None):
            raise InvalidPreferenceTimeError(
                "start_at and end_at must both be set or both be None"
            )

        # 両方ある場合のみチェック
        if start_at is not None and end_at is not None:
            if start_at >= end_at:
                raise InvalidPreferenceTimeError(
                    "start_at must be earlier than end_at"
                )

    # ------------------------------------------
    # create
    # ------------------------------------------
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        preference_in: ShiftPreferenceCreate,
    ) -> ShiftPreference:

        user = await db.get(User, user_id)
        if user is None:
            raise UserNotFoundError()

        ShiftPreferenceService._validate_time_range(
            preference_in.start_at,
            preference_in.end_at,
        )

        preference = ShiftPreference(
            user_id=user_id,
            shift_slot_id=preference_in.shift_slot_id,
            target_date=preference_in.target_date,
            start_at=preference_in.start_at,
            end_at=preference_in.end_at,
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
    async def get_all(
        db: AsyncSession,
    ) -> list[ShiftPreference]:

        result = await db.scalars(select(ShiftPreference))
        return result.all()

    # ------------------------------------------
    # get by id
    # ------------------------------------------
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        preference_id: int,
    ) -> ShiftPreference:

        preference = await db.get(
            ShiftPreference,
            preference_id,
        )

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

        update_data = preference_in.model_dump(
            exclude_unset=True
        )

        new_start = update_data.get(
            "start_at",
            preference.start_at,
        )
        new_end = update_data.get(
            "end_at",
            preference.end_at,
        )

        ShiftPreferenceService._validate_time_range(
            new_start,
            new_end,
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