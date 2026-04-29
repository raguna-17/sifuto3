from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from enum import Enum

from app.recruiting.job_applications.model import JobApplication
from app.recruiting.job_applications.schema import JobApplicationCreate, JobApplicationUpdate
from app.recruiting.job_postings.model import JobPosting
from app.recruiting.users.model import User

from app.recruiting.job_applications import repository


# =====================
# ステータス定義
# =====================
class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


# =====================
# 応募
# =====================
async def apply_to_job(
    db: AsyncSession,
    data: JobApplicationCreate,
    current_user: User,
) -> JobApplication:

    # 求人存在チェック
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == data.job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    # 重複応募チェック
    exists = await repository.exists_by_user_and_job(
        db, current_user.id, data.job_posting_id
    )
    if exists:
        raise HTTPException(400, "Already applied")

    application = JobApplication(
        user_id=current_user.id,
        job_posting_id=data.job_posting_id,
        status=ApplicationStatus.APPLIED.value,
    )

    return await repository.create(db, application)


# =====================
# 自分の応募一覧
# =====================
async def get_my_applications(
    db: AsyncSession,
    current_user: User,
):
    return await repository.get_by_user(db, current_user.id)


# =====================
# 求人ごとの応募一覧（企業側）
# =====================
async def get_applications_for_job(
    db: AsyncSession,
    job_posting_id: int,
    current_user: User,
):
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    # 🔐 自分の求人だけ見れる
    if job.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    return await repository.get_by_job(db, job_posting_id)


# =====================
# ステータス更新（ここが評価ポイント）
# =====================
async def update_application_status(
    db: AsyncSession,
    application_id: int,
    data: JobApplicationUpdate,
    current_user: User,
) -> JobApplication:

    application = await repository.get_by_id(db, application_id)

    if application is None:
        raise HTTPException(404, "Application not found")

    # JobPosting取得（認可用）
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == application.job_posting_id)
    )
    job = result.scalars().first()

    if job is None:
        raise HTTPException(404, "JobPosting not found")

    if job.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    # ステータス遷移制御（業務ロジック）
    if data.status is not None:

        allowed_transitions = {
            ApplicationStatus.APPLIED.value: [
                ApplicationStatus.INTERVIEW.value,
                ApplicationStatus.REJECTED.value,
            ],
            ApplicationStatus.INTERVIEW.value: [
                ApplicationStatus.OFFER.value,
                ApplicationStatus.REJECTED.value,
            ],
            ApplicationStatus.OFFER.value: [],
            ApplicationStatus.REJECTED.value: [],
        }

        current_status = application.status

        if data.status not in allowed_transitions.get(current_status, []):
            raise HTTPException(400, "Invalid status transition")

        application.status = data.status

    await db.commit()
    await db.refresh(application)

    return application