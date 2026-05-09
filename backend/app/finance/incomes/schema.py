from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# base
# -------------------------

class IncomeBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    amount: int = Field(gt=0)


# -------------------------
# create
# -------------------------

class IncomeCreate(IncomeBase):
    pass


# -------------------------
# update
# -------------------------

class IncomeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    amount: int | None = Field(default=None, gt=0)


# -------------------------
# response
# -------------------------

class IncomeResponse(IncomeBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)