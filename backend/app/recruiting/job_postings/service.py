from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.recruiting.job_postings.model import JobPosting
from app.recruiting.job_postings.schema import (
    JobPostingCreate,
    JobPostingUpdate,
)
from app.recruiting.organizations.model import Organization
from app.recruiting.users.model import User


# ===== 作成 =====
async def create_job_posting(
    db: AsyncSession,
    data: JobPostingCreate,
    current_user: User,
) -> JobPosting:

    # ✅ organization存在チェック
    org_result = await db.execute(
        select(Organization).where(Organization.id == data.organization_id)
    )
    org = org_result.scalars().first()

    if org is None:
        raise HTTPException(404, "Organization not found")

    job = JobPosting(
        **data.model_dump(),
        user_id=current_user.id,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    return job


# ===== 更新 =====
async def update_job_posting(
    db: AsyncSession,
    job_posting_id: int,
    data: JobPostingUpdate,
    current_user: User,
) -> JobPosting:

    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    # ✅ 認可
    if job.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    update_data = data.model_dump(exclude_unset=True)

    # ❌ organization_idは更新させない（念のためガード）
    update_data.pop("organization_id", None)

    for key, value in update_data.items():
        setattr(job, key, value)

    await db.commit()
    await db.refresh(job)

    return job


# ===== 非アクティブ化 =====
async def deactivate_job_posting(
    db: AsyncSession,
    job_posting_id: int,
    current_user: User,
) -> None:

    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    if job.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    job.is_active = False

    await db.commit()


# ===== 一覧 =====
async def get_job_postings(db: AsyncSession):
    result = await db.execute(
        select(JobPosting).where(JobPosting.is_active == True)
    )
    return result.scalars().all()

# 詳細
async def get_job_posting(
    db: AsyncSession,
    job_posting_id: int,
) -> JobPosting:

    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    return job