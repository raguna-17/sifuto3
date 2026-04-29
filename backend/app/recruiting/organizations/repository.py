from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .model import Organization
from .schema import OrganizationCreate, OrganizationUpdate


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ===== 取得（単体）=====
    async def get_by_id(self, org_id: int) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    # ===== 一覧取得 =====
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .order_by(Organization.id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    # ===== 作成 =====
    async def create(self, data: OrganizationCreate) -> Organization:
        org = Organization(**data.model_dump())

        self.db.add(org)
        await self.db.commit()
        await self.db.refresh(org)

        return org

    # ===== 更新（部分更新対応）=====
    async def update(
        self,
        org: Organization,
        data: OrganizationUpdate
    ) -> Organization:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(org, key, value)

        await self.db.commit()
        await self.db.refresh(org)

        return org

    # ===== 削除 =====
    async def delete(self, org: Organization) -> None:
        await self.db.delete(org)
        await self.db.commit()

    # ===== 名前検索（実務でほぼ必須）=====
    async def search_by_name(self, keyword: str) -> list[Organization]:
        result = await self.db.execute(
            select(Organization).where(
                Organization.name.ilike(f"%{keyword}%")
            )
        )
        return result.scalars().all()