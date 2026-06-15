from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ShiftStatus


# =========================
# base
# =========================
class ShiftAssignmentBase(BaseModel):
    slot_id: int


# =========================
# create
# =========================
class ShiftAssignmentCreate(BaseModel):
    slot_id: int

    # admin用 or auto assignment用
    user_id: int | None = None

    is_auto: bool = True


# =========================
# update
# =========================
class ShiftAssignmentUpdate(BaseModel):
    is_auto: bool | None = None
    status: ShiftStatus | None = None


# =========================
# response
# =========================
class ShiftAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int
    slot_id: int

    is_auto: bool
    status: ShiftStatus