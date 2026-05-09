from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user

from app.finance.categories import service
from app.finance.categories.schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryAdminResponse,
)

router = APIRouter(prefix="/categories", tags=["categories"])


# -------------------------
# create
# -------------------------

@router.post(
    "",
    response_model=CategoryResponse,
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    category = await service.create_category(
        db=db,
        name=data.name,
        user_id=user.id,
    )

    return category


# -------------------------
# list
# -------------------------

@router.get(
    "",
    response_model=list[CategoryResponse],
)
async def list_categories(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.list_categories(
        db=db,
        user_id=user.id,
    )


# -------------------------
# get one
# -------------------------

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    category = await service.get_category(
        db=db,
        category_id=category_id,
        user_id=user.id,
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


# -------------------------
# delete
# -------------------------

@router.delete(
    "/{category_id}",
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    success = await service.delete_category(
        db=db,
        category_id=category_id,
        user_id=user.id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return {"ok": True}