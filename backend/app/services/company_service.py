from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Company


async def get_companies(db: AsyncSession):
    result = await db.execute(select(Company))
    return result.scalars().all()


async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )
    return result.scalars().first()


async def get_company_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(Company).where(Company.name == name)
    )
    return result.scalars().first()


async def create_company(db: AsyncSession, data: dict):
    new_company = Company(**data)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company


async def delete_company(db: AsyncSession, company_id: int):
    company = await get_company(db, company_id)
    if not company:
        return None

    await db.delete(company)
    await db.commit()
    return company