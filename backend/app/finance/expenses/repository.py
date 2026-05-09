from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.finance.expenses.model import Expense
from app.finance.expenses.schema import ExpenseCreate, ExpenseUpdate


# -------------------------
# create
# -------------------------

async def create_expense(
    db: AsyncSession,
    user_id: int,
    data: ExpenseCreate,
) -> Expense:
    expense = Expense(
        title=data.title,
        amount=data.amount,
        category_id=data.category_id,
        user_id=user_id,
    )

    db.add(expense)
    await db.commit()
    await db.refresh(expense)

    return expense


# -------------------------
# get list (user only)
# -------------------------

async def get_expenses_by_user(
    db: AsyncSession,
    user_id: int,
):
    result = await db.execute(
        select(Expense)
        .where(Expense.user_id == user_id)
        .order_by(Expense.created_at.desc())
    )

    return result.scalars().all()


# -------------------------
# get single
# -------------------------

async def get_expense_by_id(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
):
    result = await db.execute(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()


# -------------------------
# update
# -------------------------

async def update_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
    data: ExpenseUpdate,
):
    expense = await get_expense_by_id(db, expense_id, user_id)

    if not expense:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)

    await db.commit()
    await db.refresh(expense)

    return expense


# -------------------------
# delete
# -------------------------

async def delete_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int,
):
    expense = await get_expense_by_id(db, expense_id, user_id)

    if not expense:
        return False

    await db.delete(expense)
    await db.commit()

    return True