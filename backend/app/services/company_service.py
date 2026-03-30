from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status
from app.models import Company, Application, User
from app.auth import get_current_user
from app.db import get_db
from app.enums import ApplicationStatus


# -----------------
# 認証付きCRUD: Company
# -----------------

async def get_companies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Company).options(selectinload(Company.applications))
    )
    return result.scalars().all()


async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Company)
        .options(selectinload(Company.applications))
        .where(Company.id == company_id)
    )
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


async def get_company_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Company).where(Company.name == name)
    )
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


async def create_company(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_company = Company(**data)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company


async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = await get_company(company_id, db, current_user)
    await db.delete(company)
    await db.commit()
    return company


# -----------------
# 認証付き: Application作成（応募）
# -----------------

async def create_application(
    user: User = Depends(get_current_user),
    company_data: dict = None,  # {"name": ..., "industry": ...}
    position: str = None,
    db: AsyncSession = Depends(get_db)
):
    if company_data is None or position is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="company data and position required")

    # 会社作成（既存チェック不要）
    company = Company(**company_data)
    db.add(company)
    await db.commit()
    await db.refresh(company)

    # 二重応募チェック
    result = await db.execute(
        select(Application).where(
            Application.user_id == user.id,
            Application.company_id == company.id,
        )
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この会社にはすでに応募済みです"
        )

    # 応募作成
    new_app = Application(
        user_id=user.id,
        company_id=company.id,
        position=position,
        status=ApplicationStatus.APPLIED
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app


# -----------------
# 応募一覧取得
# -----------------
async def get_user_applications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.company))
        .where(Application.user_id == user.id)
    )
    return result.scalars().all()