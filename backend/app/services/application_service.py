from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status

from app.models import Application, Company, User
from app.auth import get_current_user
from app.db import get_db
from app.enums import ApplicationStatus


# -----------------
# 応募一覧取得
# -----------------
async def get_user_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.notes))
        .where(Application.user_id == current_user.id)
    )
    return result.scalars().all()


# -----------------
# 単体応募取得
# -----------------
async def get_user_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.notes))
        .where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return app


# -----------------
# 応募作成
# -----------------
async def create_user_application(
    company_data: dict,   # {"name": ..., "industry": ...}
    position: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not company_data or not position:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company data and position are required")

    # 会社作成（既存チェック不要）
    company = Company(**company_data)
    db.add(company)
    await db.commit()
    await db.refresh(company)

    # 二重応募チェック
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
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
        user_id=current_user.id,
        company_id=company.id,
        position=position,
        status=ApplicationStatus.APPLIED
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)

    # 応募＋notesを再取得して返す
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.notes))
        .where(Application.id == new_app.id)
    )
    return result.scalars().first()


# -----------------
# 応募削除
# -----------------
async def delete_user_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app = await get_user_application(application_id, db, current_user)
    await db.delete(app)
    await db.commit()
    return app