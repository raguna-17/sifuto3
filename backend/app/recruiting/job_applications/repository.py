from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, exists

from app.recruiting.job_applications.model import JobApplication


async def create(
    db: AsyncSession,
    application: JobApplication,
) -> JobApplication:
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


async def get_by_id(
    db: AsyncSession,
    application_id: int,
) -> JobApplication | None:
    result = await db.execute(
        select(JobApplication).where(JobApplication.id == application_id)
    )
    return result.scalars().first()


async def get_by_user(
    db: AsyncSession,
    user_id: int,
):
    result = await db.execute(
        select(JobApplication)
        .where(JobApplication.user_id == user_id)
        .order_by(desc(JobApplication.created_at))
    )
    return result.scalars().all()


async def get_by_job(
    db: AsyncSession,
    job_posting_id: int,
):
    result = await db.execute(
        select(JobApplication)
        .where(JobApplication.job_posting_id == job_posting_id)
        .order_by(desc(JobApplication.created_at))
    )
    return result.scalars().all()


async def exists_by_user_and_job(
    db: AsyncSession,
    user_id: int,
    job_posting_id: int,
) -> bool:
    result = await db.execute(
        select(exists().where(
            JobApplication.user_id == user_id,
            JobApplication.job_posting_id == job_posting_id
        ))
    )
    return result.scalar()