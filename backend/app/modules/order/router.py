from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user, require_role

from app.modules.order import service
from app.modules.order.schema import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)

router = APIRouter(prefix="/orders", tags=["orders"])


# -------------------------
# 👤 ユーザー：注文作成
# -------------------------

@router.post("/", response_model=OrderResponse)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    # ここで本来は product価格取得して total_price計算するべきだが
    # MVPなのでserviceに丸投げ前提
    return await service.create_order(
        db=db,
        user_id=user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        total_price=0,  # ←本来は計算必須（後で改善ポイント）
    )


# -------------------------
# 👤 ユーザー：自分の注文一覧
# -------------------------

@router.get("/", response_model=list[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    return await service.get_user_orders(db, user.id)


# -------------------------
# 👤 ユーザー：注文詳細（自分のみ）
# -------------------------

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    order = await service.get_order_detail(db, order_id, user.id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -------------------------
# 👤 ユーザー：キャンセル（pendingのみ想定）
# -------------------------

@router.delete("/{order_id}")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    order = await service.get_order_detail(db, order_id, user.id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot cancel this order")

    await service.delete_order(db, order_id)

    return {"message": "canceled"}


# =========================================================
# 🛠 ADMIN ROUTES
# =========================================================


# -------------------------
# 管理：全注文取得
# -------------------------

@router.get("/admin/all", response_model=list[OrderResponse])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_role("admin")),
):
    return await service.get_all_orders(db)


# -------------------------
# 管理：ステータス更新
# -------------------------

@router.patch("/admin/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    payload: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_role("admin")),
):
    order = await service.update_order_status(
        db=db,
        order_id=order_id,
        status=payload.status,
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -------------------------
# 管理：削除
# -------------------------

@router.delete("/admin/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_role("admin")),
):
    result = await service.delete_order(db, order_id)

    if not result:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "deleted"}