from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models import Application, Company, User
from app.enums import ApplicationStatus


# -----------------
# 応募一覧取得
# -----------------
async def get_user_applications(db: AsyncSession, current_user: User):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.company))
        .where(Application.user_id == current_user.id)
    )
    return result.scalars().all()


# -----------------
# 単体応募取得
# -----------------
async def get_user_application(application_id: int, db: AsyncSession, current_user: User):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.company))
        .where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )
    app = result.scalars().first()

    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return app


# -----------------
# 応募作成（修正版）
# -----------------
async def create_user_application(db: AsyncSession, user: User, company_data: dict, position: str):
    company_name = company_data.get("name", "").strip()

    if not company_name or not position:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Company name and position are required"
        )

    # 🔥 会社を再利用（ここが最重要）
    result = await db.execute(
        select(Company).where(Company.name == company_name)
    )
    company = result.scalars().first()

    if not company:
        company = Company(**company_data)
        db.add(company)
        await db.commit()
        await db.refresh(company)

    # 🔥 重複チェック（company + position）
    result = await db.execute(
        select(Application).where(
            Application.user_id == user.id,
            Application.company_id == company.id,
            Application.position == position
        )
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="同じ会社・同じポジションには既に応募済みです"
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

    # company付きで返す
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.company))
        .where(Application.id == new_app.id)
    )
    return result.scalars().first()


# -----------------
# 応募削除
# -----------------
async def delete_user_application(application_id: int, db: AsyncSession, current_user: User):
    app = await get_user_application(application_id, db, current_user)

    await db.delete(app)
    await db.commit()

    return app


# -----------------
# ステータス更新
# -----------------
async def update_application_status(application_id: int, status: str, db: AsyncSession, user: User):
    app = await get_user_application(application_id, db, user)

    try:
        new_status = ApplicationStatus(status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid status value"
        )

    app.status = new_status

    await db.commit()
    await db.refresh(app)

    result = await db.execute(
        select(Application)
        .options(selectinload(Application.company))
        .where(Application.id == app.id)
    )
    return result.scalars().first()