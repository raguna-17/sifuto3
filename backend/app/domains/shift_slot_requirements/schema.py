from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ShiftSlotRequirementBase(BaseModel):
    position_id: int

    required_count: int = Field(
        ...,
        ge=1,
    )


class ShiftSlotRequirementCreate(
    ShiftSlotRequirementBase
):
    pass


class ShiftSlotRequirementUpdate(
    BaseModel
):
    required_count: int | None = Field(
        default=None,
        ge=1,
    )


class ShiftSlotRequirementResponse(
    ShiftSlotRequirementBase
):
    id: int
    slot_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
