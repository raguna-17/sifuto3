from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.organizations.model import Organization
from app.organizations.schema import OrganizationCreate


# 企業作成
async def create_organization(
    db: AsyncSession,
    user_id: int,
    org_in: OrganizationCreate,
) -> Organization:
    org = Organization(
        name=org_in.name,
        industry=org_in.industry,
        user_id=user_id,
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


# 全件取得（ユーザー単位）
async def get_organizations(
    db: AsyncSession,
    user_id: int,
) -> list[Organization]:
    result = await db.execute(
        select(Organization).where(Organization.user_id == user_id)
    )
    return result.scalars().all()


# 単体取得
async def get_organization_by_id(
    db: AsyncSession,
    org_id: int,
) -> Organization:
    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org


# 削除
async def delete_organization(
    db: AsyncSession,
    org_id: int,
) -> None:
    org = await get_organization_by_id(db, org_id)

    await db.delete(org)
    await db.commit()