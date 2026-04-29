from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

from app.recruiting.organizations.schema import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.recruiting.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# ===== Service生成 =====
def get_org_service(db: AsyncSession = Depends(get_db)):
    return OrganizationService(db)


# ===== 作成 =====
@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    data: OrganizationCreate,
    service: OrganizationService = Depends(get_org_service),
):
    return await service.create_organization(data)


# ===== 一覧 =====
@router.get("/", response_model=list[OrganizationResponse])
async def list_organizations(
    service: OrganizationService = Depends(get_org_service),
):
    return await service.list_organizations()


# ===== 詳細取得 =====
@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    service: OrganizationService = Depends(get_org_service),
):
    return await service.get_organization(org_id)


# ===== 更新 =====
@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    data: OrganizationUpdate,
    service: OrganizationService = Depends(get_org_service),
):
    return await service.update_organization(org_id, data)


# ===== 削除 =====
@router.delete("/{org_id}")
async def delete_organization(
    org_id: int,
    service: OrganizationService = Depends(get_org_service),
):
    await service.delete_organization(org_id)
    return {"message": "deleted"}