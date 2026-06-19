from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import PreferencePriority


# =========================
# base
# =========================
class ShiftPreferenceBase(BaseModel):
    shift_slot_id: int

    priority: PreferencePriority = (
        PreferencePriority.NEUTRAL
    )

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
    priority: PreferencePriority | None = None
    note: str | None = None


# =========================
# response
# =========================
class ShiftPreferenceResponse(
    ShiftPreferenceBase
):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime