from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user

from app.modules.cart import service
from app.modules.cart.schema import (
    CartCreate,
    CartUpdate,
    CartItemResponse,
)

router = APIRouter(prefix="/cart", tags=["cart"])


# -------------------------
# カート一覧取得
# -------------------------

@router.get("/", response_model=list[CartItemResponse])
async def get_cart_items(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    return await service.get_cart(db, user.id)


# -------------------------
# 商品追加
# -------------------------

@router.post("/", response_model=CartItemResponse)
async def add_item_to_cart(
    payload: CartCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    return await service.add_to_cart(
        db=db,
        user_id=user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
    )


# -------------------------
# 数量更新
# -------------------------

@router.patch("/{product_id}", response_model=CartItemResponse)
async def update_cart_item(
    product_id: int,
    payload: CartUpdate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    result = await service.update_cart(
        db=db,
        user_id=user.id,
        product_id=product_id,
        quantity=payload.quantity,
    )

    if not result:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return result


# -------------------------
# 削除
# -------------------------

@router.delete("/{product_id}")
async def delete_cart_item(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    result = await service.remove_from_cart(
        db=db,
        user_id=user.id,
        product_id=product_id,
    )

    if not result:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "deleted"}


# -------------------------
# カート全削除
# -------------------------

@router.delete("/")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    await service.clear_cart(db, user.id)
    return {"message": "cleared"}