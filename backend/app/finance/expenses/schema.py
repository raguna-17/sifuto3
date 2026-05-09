from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# base
# -------------------------

class ExpenseBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    amount: int = Field(gt=0)
    category_id: int | None = Field(default=None)


# -------------------------
# create
# -------------------------

class ExpenseCreate(ExpenseBase):
    pass


# -------------------------
# update
# -------------------------

class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    amount: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None)


# -------------------------
# response
# -------------------------

class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)