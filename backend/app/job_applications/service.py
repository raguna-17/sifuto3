from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.job_applications.model import JobApplication
from app.job_applications.schema import JobApplicationCreate
from app.organizations.model import Organization


# =========================
# 作成
# =========================
async def create_job_application(
    db: AsyncSession,
    user_id: int,
    job_in: JobApplicationCreate,
) -> JobApplication:

    # 企業存在チェック
    org_result = await db.execute(
        select(Organization).where(
            Organization.id == job_in.organization_id
        )
    )
    organization = org_result.scalar_one_or_none()

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    job = JobApplication(
        user_id=user_id,
        organization_id=job_in.organization_id,
        organization_name=organization.name,
        job_title=job_in.job_title,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    return job


# =========================
# 一覧取得（ユーザー単位）
# =========================
async def get_job_applications(
    db: AsyncSession,
    user_id: int,
) -> list[JobApplication]:

    result = await db.execute(
        select(JobApplication).where(
            JobApplication.user_id == user_id
        )
    )

    return list(result.scalars().all())


# =========================
# 単体取得
# =========================
async def get_job_application_by_id(
    db: AsyncSession,
    job_id: int,
    user_id: int,
) -> JobApplication:

    result = await db.execute(
        select(JobApplication).where(
            JobApplication.id == job_id,
            JobApplication.user_id == user_id,
        )
    )

    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    return job


# =========================
# 削除
# =========================
async def delete_job_application(
    db: AsyncSession,
    job_id: int,
    user_id: int,
) -> None:

    job = await get_job_application_by_id(db, job_id, user_id)

    await db.delete(job)
    await db.commit()