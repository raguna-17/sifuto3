from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.model import User
from app.domains.shift_preferences.model import ShiftPreference
from app.domains.shift_preferences.schema import (
    ShiftPreferenceCreate,
    ShiftPreferenceUpdate,
)


class ShiftPreferenceNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidPreferenceTimeError(Exception):
    pass


class ShiftPreferenceService:

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        preference_in: ShiftPreferenceCreate,
    ) -> ShiftPreference:

        user = await db.get(User, user_id)

        if not user:
            raise UserNotFoundError()

        if (
            preference_in.start_at
            and preference_in.end_at
            and preference_in.start_at >= preference_in.end_at
        ):
            raise InvalidPreferenceTimeError()

        preference = ShiftPreference(
            user_id=user_id,
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

    @staticmethod
    async def get_all(db: AsyncSession) -> list[ShiftPreference]:

        result = await db.scalars(select(ShiftPreference))
        return list(result)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        preference_id: int,
    ) -> ShiftPreference:

        preference = await db.get(ShiftPreference, preference_id)

        if not preference:
            raise ShiftPreferenceNotFoundError()

        return preference

    @staticmethod
    async def get_by_user(
        db: AsyncSession,
        user_id: int,
    ) -> list[ShiftPreference]:

        result = await db.execute(
            select(ShiftPreference).where(
                ShiftPreference.user_id == user_id
            )
        )

        return list(result.scalars().all())

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

        new_start = update_data.get("start_at", preference.start_at)
        new_end = update_data.get("end_at", preference.end_at)

        if (
            new_start
            and new_end
            and new_start >= new_end
        ):
            raise InvalidPreferenceTimeError()

        for field, value in update_data.items():
            setattr(preference, field, value)

        try:
            await db.commit()
            await db.refresh(preference)
            return preference

        except Exception:
            await db.rollback()
            raise

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

