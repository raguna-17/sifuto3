from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.recruiting.organizations.repository import OrganizationRepository
from app.recruiting.organizations.schema import OrganizationCreate, OrganizationUpdate


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.repo = OrganizationRepository(db)

    # ===== 取得（単体）=====
    async def get_organization(self, org_id: int):
        org = await self.repo.get_by_id(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return org

    # ===== 一覧 =====
    async def list_organizations(self, limit: int = 100, offset: int = 0):
        return await self.repo.get_all(limit=limit, offset=offset)

    # ===== 作成 =====
    async def create_organization(self, data: OrganizationCreate):
        try:
            await self._validate_name(data.name)
            return await self.repo.create(data)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        except IntegrityError:
            await self.repo.db.rollback()
            raise HTTPException(status_code=400, detail="Organization already exists")

    # ===== 更新 =====
    async def update_organization(self, org_id: int, data: OrganizationUpdate):
        org = await self.repo.get_by_id(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        try:
            if data.name:
                await self._validate_name(data.name)

            return await self.repo.update(org, data)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        except IntegrityError:
            await self.repo.db.rollback()
            raise HTTPException(status_code=400, detail="Organization already exists")

    # ===== 削除 =====
    async def delete_organization(self, org_id: int):
        org = await self.repo.get_by_id(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        await self.repo.delete(org)

    # ===== 検索 =====
    async def search_organizations(self, keyword: str):
        return await self.repo.search_by_name(keyword)

    # ===== バリデーション =====
    async def _validate_name(self, name: str):
        if len(name) < 2:
            raise ValueError("Organization name too short")

        existing = await self.repo.search_by_name(name)

        for org in existing:
            if org.name.lower() == name.lower():
                raise ValueError("Organization already exists")