from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.finance.incomes.model import Income
from app.finance.incomes.schema import IncomeCreate, IncomeUpdate


# -------------------------
# create
# -------------------------

async def create_income(
    db: AsyncSession,
    user_id: int,
    data: IncomeCreate,
) -> Income:
    income = Income(
        title=data.title,
        amount=data.amount,
        user_id=user_id,
    )

    db.add(income)
    await db.commit()
    await db.refresh(income)

    return income


# -------------------------
# list
# -------------------------

async def get_incomes_by_user(
    db: AsyncSession,
    user_id: int,
):
    result = await db.execute(
        select(Income)
        .where(Income.user_id == user_id)
        .order_by(Income.created_at.desc())
    )

    return result.scalars().all()


# -------------------------
# single
# -------------------------

async def get_income_by_id(
    db: AsyncSession,
    income_id: int,
    user_id: int,
):
    result = await db.execute(
        select(Income).where(
            Income.id == income_id,
            Income.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()


# -------------------------
# update
# -------------------------

async def update_income(
    db: AsyncSession,
    income_id: int,
    user_id: int,
    data: IncomeUpdate,
):
    income = await get_income_by_id(db, income_id, user_id)

    if not income:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(income, key, value)

    await db.commit()
    await db.refresh(income)

    return income


# -------------------------
# delete
# -------------------------

async def delete_income(
    db: AsyncSession,
    income_id: int,
    user_id: int,
):
    income = await get_income_by_id(db, income_id, user_id)

    if not income:
        return False

    await db.delete(income)
    await db.commit()

    return True