from pydantic import BaseModel, ConfigDict


# =========================
# create
# =========================
class ShiftAssignmentCreate(BaseModel):
    slot_id: int


# =========================
# update (admin only想定)
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