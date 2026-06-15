from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enums import PositionType


# ==========================================
# Base
# ==========================================

class ShiftSlotBase(BaseModel):
    start_at: datetime
    end_at: datetime

    required_staff_count: int = Field(
        ge=1,
        description="必要人数（1以上）",
    )

    required_position: PositionType


    @model_validator(mode="after")
    def validate_time_range(self):
        # 単体データとしての整合性だけ見る
        if self.start_at >= self.end_at:
            raise ValueError("start_at must be earlier than end_at")

        return self


# ==========================================
# Create
# ==========================================

class ShiftSlotCreate(ShiftSlotBase):
    pass


# ==========================================
# Update
# ==========================================

class ShiftSlotUpdate(BaseModel):
    start_at: datetime | None = None
    end_at: datetime | None = None

    required_staff_count: int | None = Field(
        default=None,
        ge=1,
    )

    required_position: PositionType | None = None

    @model_validator(mode="after")
    def validate_time_range(self):
        # updateはpartialなので両方揃ってる時だけチェック
        if self.start_at is not None and self.end_at is not None:
            if self.start_at >= self.end_at:
                raise ValueError("start_at must be earlier than end_at")

        return self


# ==========================================
# Response
# ==========================================

class ShiftSlotResponse(ShiftSlotBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# List（軽量版）
# ==========================================

class ShiftSlotListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    start_at: datetime
    end_at: datetime
    required_staff_count: int
    required_position: PositionType