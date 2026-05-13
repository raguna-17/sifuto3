from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# 共通
# -------------------------

class OrderBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


# -------------------------
# 作成
# -------------------------

class OrderCreate(OrderBase):
    pass


# -------------------------
# 更新（ステータス変更用）
# -------------------------

class OrderUpdate(BaseModel):
    status: str


# -------------------------
# レスポンス
# -------------------------

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)