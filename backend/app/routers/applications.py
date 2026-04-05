from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.models import User
from app.schemas import (
    ApplicationRead,
    ApplicationCreateRequest,
    ApplicationStatusUpdate  # ← 追加
)
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
    try:
        return await application_service.get_user_applications(db, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch applications: {str(e)}")


# -----------------
# 単体応募取得
# -----------------
@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        app = await application_service.get_user_application(application_id, db, current_user)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        return app
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch application: {str(e)}")


# -----------------
# 応募作成
# -----------------
@router.post("/", response_model=ApplicationRead, status_code=201)
async def create_application(
    payload: ApplicationCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await application_service.create_user_application(
            db=db,
            user=current_user,
            company_data={
                "name": payload.company_name,
                "industry": payload.industry
            },
            position=payload.position
        )
    except HTTPException:
        raise
    except RequestValidationError:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create application: {str(e)}")


# -----------------
# 応募削除
# -----------------
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        app = await application_service.delete_user_application(application_id, db, current_user)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete application: {str(e)}")


# -----------------
# ステータス更新（←これが今回の本命）
# -----------------
@router.patch("/{application_id}", response_model=ApplicationRead)
async def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        app = await application_service.update_application_status(
            application_id=application_id,
            status=payload.status,
            db=db,
            user=current_user
        )

        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        return app

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")