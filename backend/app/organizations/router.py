from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.dependencies import get_current_active_user
from app.users.model import User

from app.organizations.schema import (
    OrganizationCreate,
    OrganizationResponse,
)

from app.organizations import service as org_service

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# 作成
@router.post("", response_model=OrganizationResponse)
async def create_organization(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await org_service.create_organization(
        db=db,
        user_id=current_user.id,
        org_in=org_in,
    )


# 一覧取得（自分の企業）
@router.get("", response_model=list[OrganizationResponse])
async def get_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await org_service.get_organizations(
        db=db,
        user_id=current_user.id,
    )


# 単体取得
@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await org_service.get_organization_by_id(
        db=db,
        org_id=org_id,
    )


# 削除
@router.delete("/{org_id}")
async def delete_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await org_service.delete_organization(
        db=db,
        org_id=org_id,
    )
    return {"message": "deleted"}