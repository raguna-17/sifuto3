from sqlalchemy.ext.asyncio import AsyncSession

from app.finance.expenses import repository
from app.finance.expenses.schema import ExpenseCreate, ExpenseUpdate


# -------------------------
# create
# -------------------------

async def create_expense(
    db: AsyncSession,
    user_id: int,
    data: ExpenseCreate,
):
    # ここに「ビジネスルール」を入れる場所
    # 例：上限チェックとか、カテゴリ存在チェックとか

    return await repository.create_expense(
        db=db,
        user_id=user_id,
        data=data,
    )


# -------------------------
# get list
# -------------------------

async def get_expenses(
    db: AsyncSession,
    user_id: int,
):
    return await repository.get_expenses_by_user(
        db=db,
        user_id=user_id,
    )


# -------------------------
# get single
# -------------------------

async def get_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
):
    return await repository.get_expense_by_id(
        db=db,
        expense_id=expense_id,
        user_id=user_id,
    )


# -------------------------
# update
# -------------------------

async def update_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
    data: ExpenseUpdate,
):
    # 例：0円更新禁止とかここで制御できる

    return await repository.update_expense(
        db=db,
        expense_id=expense_id,
        user_id=user_id,
        data=data,
    )


# -------------------------
# delete
# -------------------------

async def delete_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
):
    return await repository.delete_expense(
        db=db,
        expense_id=expense_id,
        user_id=user_id,
    )