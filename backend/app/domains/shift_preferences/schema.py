from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import PreferencePriority


# =========================
# base
# =========================
class ShiftPreferenceBase(BaseModel):
    target_date: date
    start_at: datetime | None = None
    end_at: datetime | None = None
    priority: PreferencePriority = PreferencePriority.PREFERRED
    note: str | None = None


# =========================
# create
# =========================
class ShiftPreferenceCreate(ShiftPreferenceBase):
    pass


# =========================
# update
# =========================
class ShiftPreferenceUpdate(BaseModel):
    start_at: datetime | None = None
    end_at: datetime | None = None
    priority: PreferencePriority | None = None
    note: str | None = None


# =========================
# response
# =========================
class ShiftPreferenceResponse(ShiftPreferenceBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

