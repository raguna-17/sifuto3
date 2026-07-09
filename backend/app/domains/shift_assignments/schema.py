from pydantic import BaseModel, ConfigDict


# =========================
# update
# =========================
class ShiftAssignmentUpdate(BaseModel):
    is_confirmed: bool | None = None


# =========================
# response
# =========================
class ShiftAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    slot_id: int

    is_auto: bool
    is_confirmed: bool