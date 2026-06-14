from pydantic import BaseModel, ConfigDict


# -------------------------
# base
# -------------------------
class PositionBase(BaseModel):
    name: str
    description: str | None = None


# -------------------------
# create
# -------------------------
class PositionCreate(PositionBase):
    pass


# -------------------------
# update
# -------------------------
class PositionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


# -------------------------
# response
# -------------------------
class PositionResponse(PositionBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

