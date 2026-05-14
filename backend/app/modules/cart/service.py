from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cart import repository
from app.modules.cart.model import Cart


# -------------------------
# カート取得
# -------------------------
async def get_cart(db: AsyncSession, user_id: int):
    return await repository.get_cart_items(db, user_id)


# -------------------------
# カート追加
# -------------------------
async def add_to_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int,
):
    existing = await repository.get_cart_item(db, user_id, product_id)

    if existing:
        new_qty = existing.quantity + quantity
        result = await repository.update_cart_quantity(db, existing, new_qty)
    else:
        cart = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        result = await repository.create_cart_item(db, cart)

    # ★ここが本体修正
    await db.commit()
    await db.refresh(result)

    return result


# -------------------------
# 数量更新
# -------------------------
async def update_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int,
):
    cart = await repository.get_cart_item(db, user_id, product_id)

    if not cart:
        return None

    result = await repository.update_cart_quantity(db, cart, quantity)

    await db.commit()
    await db.refresh(result)

    return result


# -------------------------
# 削除
# -------------------------
async def remove_from_cart(
    db: AsyncSession,
    user_id: int,
    product_id: int,
):
    cart = await repository.get_cart_item(db, user_id, product_id)

    if not cart:
        return None

    await repository.delete_cart_item(db, cart)

    # 削除はcommitだけ
    await db.commit()

    return True


# -------------------------
# カート全削除
# -------------------------
async def clear_cart(db: AsyncSession, user_id: int):
    await repository.clear_cart(db, user_id)

    await db.commit()

    return True