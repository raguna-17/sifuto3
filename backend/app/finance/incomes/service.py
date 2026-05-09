from sqlalchemy.ext.asyncio import AsyncSession

from app.finance.incomes import repository
from app.finance.incomes.schema import IncomeCreate, IncomeUpdate


# -------------------------
# create
# -------------------------

async def create_income(
    db: AsyncSession,
    user_id: int,
    data: IncomeCreate,
):
    # ここにビジネスルール追加できる
    # 例：収入上限チェック、ソース制限など

    return await repository.create_income(
        db=db,
        user_id=user_id,
        data=data,
    )


# -------------------------
# list
# -------------------------

async def get_incomes(
    db: AsyncSession,
    user_id: int,
):
    return await repository.get_incomes_by_user(
        db=db,
        user_id=user_id,
    )


# -------------------------
# single
# -------------------------

async def get_income(
    db: AsyncSession,
    income_id: int,
    user_id: int,
):
    return await repository.get_income_by_id(
        db=db,
        income_id=income_id,
        user_id=user_id,
    )


# -------------------------
# update
# -------------------------

async def update_income(
    db: AsyncSession,
    income_id: int,
    user_id: int,
    data: IncomeUpdate,
):
    return await repository.update_income(
        db=db,
        income_id=income_id,
        user_id=user_id,
        data=data,
    )


# -------------------------
# delete
# -------------------------

async def delete_income(
    db: AsyncSession,
    income_id: int,
    user_id: int,
):
    return await repository.delete_income(
        db=db,
        income_id=income_id,
        user_id=user_id,
    )