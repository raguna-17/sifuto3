from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.core.enums import ShiftStatus


class ShiftAssignmentBase(BaseModel):
    user_id: int
    slot_id: int


class ShiftAssignmentCreate(
    ShiftAssignmentBase
):
    is_auto: bool = True


class ShiftAssignmentUpdate(
    BaseModel
):
    is_auto: bool | None = None
    status: ShiftStatus | None = None


class ShiftAssignmentResponse(
    ShiftAssignmentBase
):
    id: int
    is_auto: bool
    status: ShiftStatus

    model_config = ConfigDict(
        from_attributes=True
    )

