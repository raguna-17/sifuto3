from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.dependencies import get_current_active_user
from app.recruiting.users.model import User

from app.recruiting.job_applications import service
from app.recruiting.job_applications.schema import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
)

router = APIRouter(prefix="/job_applications", tags=["job_applications"])


@router.post("/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    data: JobApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.apply_to_job(db, data, current_user)


@router.get("/me", response_model=List[JobApplicationResponse])
async def get_my_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.get_my_applications(db, current_user)


@router.get("/job/{job_posting_id}", response_model=List[JobApplicationResponse])
async def get_applications_for_job(
    job_posting_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.get_applications_for_job(
        db, job_posting_id, current_user
    )


@router.put("/{application_id}", response_model=JobApplicationResponse)
async def update_application_status(
    application_id: int,
    data: JobApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await service.update_application_status(
        db, application_id, data, current_user
    )
