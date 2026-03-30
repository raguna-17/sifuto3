from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.models import User
from app.schemas import ApplicationRead
from app.auth import get_current_user
from app.services import application_service

router = APIRouter(prefix="/api/v1/applications", tags=["applications"])


# -----------------
# 応募一覧取得
# -----------------
@router.get("/", response_model=List[ApplicationRead])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await application_service.get_user_applications(db, current_user)


# -----------------
# 単体応募取得
# -----------------
@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    app = await application_service.get_user_application(application_id, db, current_user)

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return app


# -----------------
# 応募作成（会社名＋業界＋ポジションで送信）
# -----------------
@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application(
    company_name: str,
    industry: str | None = None,
    position: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not company_name or not position:
        raise HTTPException(status_code=400, detail="Company name and position are required")

    company_data = {"name": company_name, "industry": industry}

    return await application_service.create_user_application(
        company_data=company_data,
        position=position,
        db=db,
        current_user=current_user
    )


# -----------------
# 応募削除
# -----------------
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app = await application_service.delete_user_application(application_id, db, current_user)

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return None