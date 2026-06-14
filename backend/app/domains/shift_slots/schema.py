from datetime import datetime,date
from pydantic import BaseModel, ConfigDict


class ShiftSlotBase(BaseModel):
    target_date: date
    start_at: datetime
    end_at: datetime


class ShiftSlotCreate(ShiftSlotBase):
    pass


class ShiftSlotUpdate(BaseModel):
    start_at: datetime | None = None
    end_at: datetime | None = None


class ShiftSlotResponse(ShiftSlotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

