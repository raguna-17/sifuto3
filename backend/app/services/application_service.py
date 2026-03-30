from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Application


async def get_user_applications(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Application).where(Application.user_id == user_id)
    )
    return result.scalars().all()


async def get_user_application(db: AsyncSession, user_id: int, application_id: int):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id
        )
    )
    return result.scalars().first()


async def create_user_application(db: AsyncSession, user_id: int, data: dict):
    new_app = Application(**data, user_id=user_id)
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app


async def delete_user_application(db: AsyncSession, user_id: int, application_id: int):
    app = await get_user_application(db, user_id, application_id)
    if not app:
        return None

    await db.delete(app)
    await db.commit()
    return app