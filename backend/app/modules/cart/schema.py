from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict


# -------------------------
# 共通
# -------------------------

class CartBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, default=1)


# -------------------------
# 作成
# -------------------------

class CartCreate(CartBase):
    pass


# -------------------------
# 更新
# -------------------------

class CartUpdate(BaseModel):
    quantity: int = Field(ge=1)


# -------------------------
# レスポンス用
# -------------------------

class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)