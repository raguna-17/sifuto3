from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user

from app.finance.incomes import service
from app.finance.incomes.schema import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse,
)

router = APIRouter(prefix="/incomes", tags=["incomes"])


# -------------------------
# create income
# -------------------------

@router.post(
    "",
    response_model=IncomeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_income(
    data: IncomeCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.create_income(
        db=db,
        user_id=user.id,
        data=data,
    )


# -------------------------
# get all incomes
# -------------------------

@router.get(
    "",
    response_model=list[IncomeResponse],
)
async def get_incomes(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.get_incomes(
        db=db,
        user_id=user.id,
    )


# -------------------------
# get single income
# -------------------------

@router.get(
    "/{income_id}",
    response_model=IncomeResponse,
)
async def get_income(
    income_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    income = await service.get_income(
        db=db,
        income_id=income_id,
        user_id=user.id,
    )

    if not income:
        raise HTTPException(
            status_code=404,
            detail="Income not found",
        )

    return income


# -------------------------
# update income
# -------------------------

@router.put(
    "/{income_id}",
    response_model=IncomeResponse,
)
async def update_income(
    income_id: int,
    data: IncomeUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    income = await service.update_income(
        db=db,
        income_id=income_id,
        user_id=user.id,
        data=data,
    )

    if not income:
        raise HTTPException(
            status_code=404,
            detail="Income not found",
        )

    return income


# -------------------------
# delete income
# -------------------------

@router.delete(
    "/{income_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_income(
    income_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    ok = await service.delete_income(
        db=db,
        income_id=income_id,
        user_id=user.id,
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Income not found",
        )

    return None