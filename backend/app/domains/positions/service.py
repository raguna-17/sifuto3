from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.positions.model import Position
from app.domains.positions.schema import (
    PositionCreate,
    PositionUpdate,
)


class PositionNotFoundError(Exception):
    pass


class PositionAlreadyExistsError(Exception):
    pass


class PositionService:

    @staticmethod
    async def create(
        db: AsyncSession,
        position_in: PositionCreate,
    ) -> Position:

        existing = await db.scalar(
            select(Position).where(
                Position.name == position_in.name
            )
        )

        if existing:
            raise PositionAlreadyExistsError()

        position = Position(
            name=position_in.name,
            description=position_in.description,
        )

        try:
            db.add(position)

            await db.commit()
            await db.refresh(position)

            return position

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_all(
        db: AsyncSession,
        active_only: bool = True,
    ) -> list[Position]:

        stmt = select(Position)

        if active_only:
            stmt = stmt.where(
                Position.is_active.is_(True)
            )

        result = await db.scalars(stmt)

        return list(result)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        position_id: int,
    ) -> Position:

        position = await db.get(
            Position,
            position_id,
        )

        if not position:
            raise PositionNotFoundError()

        return position

    @staticmethod
    async def update(
        db: AsyncSession,
        position_id: int,
        position_in: PositionUpdate,
    ) -> Position:

        position = await PositionService.get_by_id(
            db=db,
            position_id=position_id,
        )

        if (
            position_in.name
            and position_in.name != position.name
        ):
            existing = await db.scalar(
                select(Position).where(
                    Position.name == position_in.name
                )
            )

            if existing:
                raise PositionAlreadyExistsError()

        update_data = (
            position_in.model_dump(
                exclude_unset=True
            )
        )

        for field, value in update_data.items():
            setattr(position, field, value)

        try:
            await db.commit()
            await db.refresh(position)

            return position

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def deactivate(
        db: AsyncSession,
        position_id: int,
    ) -> Position:

        position = await PositionService.get_by_id(
            db=db,
            position_id=position_id,
        )

        position.is_active = False

        try:
            await db.commit()
            await db.refresh(position)

            return position

        except Exception:
            await db.rollback()
            raise

