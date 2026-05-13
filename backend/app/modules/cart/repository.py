from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.modules.cart.model import Cart


# -------------------------
# 取得（ユーザーのカート一覧）
# -------------------------

async def get_cart_items(db: AsyncSession, user_id: int):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(selectinload(Cart.product))
    )

    result = await db.execute(stmt)
    return result.scalars().all()


# -------------------------
# 単一取得（商品単位）
# -------------------------

async def get_cart_item(db: AsyncSession, user_id: int, product_id: int):
    stmt = (
        select(Cart)
        .where(
            Cart.user_id == user_id,
            Cart.product_id == product_id,
        )
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# 作成
# -------------------------

async def create_cart_item(db: AsyncSession, cart: Cart):
    db.add(cart)
    await db.flush()
    return cart


# -------------------------
# 更新（数量）
# -------------------------

async def update_cart_quantity(db: AsyncSession, cart: Cart, quantity: int):
    cart.quantity = quantity
    await db.flush()
    return cart


# -------------------------
# 削除（単品）
# -------------------------

async def delete_cart_item(db: AsyncSession, cart: Cart):
    await db.delete(cart)
    await db.flush()


# -------------------------
# カート全削除
# -------------------------

async def clear_cart(db: AsyncSession, user_id: int):
    stmt = delete(Cart).where(Cart.user_id == user_id)
    await db.execute(stmt)