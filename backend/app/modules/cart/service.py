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
    # 既存チェック
    existing = await repository.get_cart_item(db, user_id, product_id)

    if existing:
        # 既にあるなら数量加算
        new_qty = existing.quantity + quantity
        return await repository.update_cart_quantity(db, existing, new_qty)

    # 新規作成
    cart = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
    )

    return await repository.create_cart_item(db, cart)


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

    return await repository.update_cart_quantity(db, cart, quantity)


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
    return True


# -------------------------
# カート全削除
# -------------------------

async def clear_cart(db: AsyncSession, user_id: int):
    await repository.clear_cart(db, user_id)
    return True