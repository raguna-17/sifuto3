from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.dependencies import get_current_active_user
from app.recruiting.users.model import User

from app.recruiting.job_postings import service
from app.recruiting.job_postings.schema import (
    JobPostingCreate,
    JobPostingUpdate,
    JobPostingResponse,
)

router = APIRouter(prefix="/job_postings", tags=["job_postings"])


# 🆕 作成
@router.post("/", response_model=JobPostingResponse, status_code=status.HTTP_201_CREATED)
async def create_job_posting(
    data: JobPostingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.create_job_posting(
        db=db,
        data=data,
        current_user=current_user,
    )


# 📄 一覧（公開）
@router.get("/", response_model=List[JobPostingResponse])
async def list_job_postings(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_job_postings(db)


# 📄 詳細
@router.get("/{job_posting_id}", response_model=JobPostingResponse)
async def get_job_posting(
    job_posting_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_job_posting(db, job_posting_id)


# ✏️ 更新
@router.put("/{job_posting_id}", response_model=JobPostingResponse)
async def update_job_posting(
    job_posting_id: int,
    data: JobPostingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.update_job_posting(
        db=db,
        job_posting_id=job_posting_id,
        data=data,
        current_user=current_user,
    )


# 🗑 論理削除
@router.delete("/{job_posting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_posting(
    job_posting_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await service.deactivate_job_posting(
        db=db,
        job_posting_id=job_posting_id,
        current_user=current_user,
    )
    return None