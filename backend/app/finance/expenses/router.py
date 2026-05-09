from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user

from app.finance.expenses import service
from app.finance.expenses.schema import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


# -------------------------
# create expense
# -------------------------

@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.create_expense(
        db=db,
        user_id=user.id,
        data=data,
    )


# -------------------------
# get all expenses
# -------------------------

@router.get(
    "",
    response_model=list[ExpenseResponse],
)
async def get_expenses(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.get_expenses(
        db=db,
        user_id=user.id,
    )


# -------------------------
# get single expense
# -------------------------

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    expense = await service.get_expense(
        db=db,
        expense_id=expense_id,
        user_id=user.id,
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense


# -------------------------
# update expense
# -------------------------

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    expense = await service.update_expense(
        db=db,
        expense_id=expense_id,
        user_id=user.id,
        data=data,
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense


# -------------------------
# delete expense
# -------------------------

@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    ok = await service.delete_expense(
        db=db,
        expense_id=expense_id,
        user_id=user.id,
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return None