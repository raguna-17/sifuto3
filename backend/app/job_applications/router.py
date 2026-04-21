from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependencies import get_current_active_user
from app.users.model import User

from app.job_applications.schema import (
    JobApplicationCreate,
    JobApplicationResponse,
)

from app.job_applications import service as job_service


router = APIRouter(
    prefix="/job-applications",
    tags=["Job Applications"],
)


# =========================
# 作成
# =========================
@router.post("", response_model=JobApplicationResponse)
async def create_job_application(
    job_in: JobApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await job_service.create_job_application(
        db=db,
        user_id=current_user.id,
        job_in=job_in,
    )


# =========================
# 一覧取得（自分の応募）
# =========================
@router.get("", response_model=list[JobApplicationResponse])
async def get_my_job_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await job_service.get_job_applications(
        db=db,
        user_id=current_user.id,
    )


# =========================
# 単体取得
# =========================
@router.get("/{job_id}", response_model=JobApplicationResponse)
async def get_job_application(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await job_service.get_job_application_by_id(
        db=db,
        job_id=job_id,
        user_id=current_user.id,
    )


# =========================
# 削除
# =========================
@router.delete("/{job_id}", status_code=204)
async def delete_job_application(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await job_service.delete_job_application(
        db=db,
        job_id=job_id,
        user_id=current_user.id,
    )
    return None