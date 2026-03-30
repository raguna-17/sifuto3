from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.models import User
from app.schemas import ApplicationRead, ApplicationCreate
from app.auth import get_current_user
from app.services import application_service

router = APIRouter(prefix="/api/v1/applications", tags=["applications"])


@router.get("/", response_model=List[ApplicationRead])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await application_service.get_user_applications(db, current_user.id)


@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    app = await application_service.get_user_application(
        db, current_user.id, application_id
    )

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return app


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await application_service.create_user_application(
        db,
        current_user.id,
        application.model_dump()
    )


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    app = await application_service.delete_user_application(
        db, current_user.id, application_id
    )

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return None