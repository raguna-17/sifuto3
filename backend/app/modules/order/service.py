from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order import repository
from app.modules.order.model import Order


# -------------------------
# 注文作成
# -------------------------

async def create_order(
    db: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int,
    total_price: int,
):
    order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price,
        status="pending",
    )

    return await repository.create_order(db, order)


# -------------------------
# ユーザー注文一覧
# -------------------------

async def get_user_orders(db: AsyncSession, user_id: int):
    return await repository.get_orders_by_user(db, user_id)


# -------------------------
# 注文詳細（所有者チェック込み）
# -------------------------

async def get_order_detail(
    db: AsyncSession,
    order_id: int,
    user_id: int,
):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return None

    # 所有者チェック（ここが重要）
    if order.user_id != user_id:
        return None

    return order


# -------------------------
# ステータス更新（基本admin用）
# -------------------------

async def update_order_status(
    db: AsyncSession,
    order_id: int,
    status: str,
):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return None

    return await repository.update_order_status(db, order, status)


# -------------------------
# 注文削除（基本admin用）
# -------------------------

async def delete_order(db: AsyncSession, order_id: int):
    order = await repository.get_order_by_id(db, order_id)

    if not order:
        return False

    await repository.delete_order(db, order)
    return True


# -------------------------
# 管理用：全注文
# -------------------------

async def get_all_orders(db: AsyncSession):
    return await repository.get_all_orders(db)