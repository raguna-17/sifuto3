from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Company

# 一覧取得（applicationsも非同期ロード済み）
async def get_companies(db: AsyncSession):
    result = await db.execute(
        select(Company).options(selectinload(Company.applications))
    )
    return result.scalars().all()

# 単体取得（applicationsも非同期ロード済み）
async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(Company)
        .options(selectinload(Company.applications))
        .where(Company.id == company_id)
    )
    return result.scalars().first()

# 名前検索（applicationsロード不要）
async def get_company_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(Company).where(Company.name == name)
    )
    return result.scalars().first()

# 作成
async def create_company(db: AsyncSession, data: dict):
    new_company = Company(**data)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

# 削除
async def delete_company(db: AsyncSession, company_id: int):
    company = await get_company(db, company_id)
    if not company:
        return None
    await db.delete(company)
    await db.commit()
    return company