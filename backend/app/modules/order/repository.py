from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.modules.order.model import Order


# -------------------------
# 単一取得（注文詳細）
# -------------------------

async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id)

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# -------------------------
# ユーザーの注文一覧
# -------------------------

async def get_orders_by_user(db: AsyncSession, user_id: int):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )

    result = await db.execute(stmt)
    return result.scalars().all()


# -------------------------
# 作成
# -------------------------

async def create_order(db: AsyncSession, order: Order):
    db.add(order)
    await db.flush()
    return order


# -------------------------
# ステータス更新
# -------------------------

async def update_order_status(db: AsyncSession, order: Order, status: str):
    order.status = status
    await db.flush()
    return order


# -------------------------
# 削除（基本は管理用）
# -------------------------

async def delete_order(db: AsyncSession, order: Order):
    await db.delete(order)
    await db.flush()


# -------------------------
# 管理用：全注文取得
# -------------------------

async def get_all_orders(db: AsyncSession):
    stmt = select(Order).order_by(Order.created_at.desc())

    result = await db.execute(stmt)
    return result.scalars().all()