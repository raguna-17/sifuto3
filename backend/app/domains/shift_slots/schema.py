from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ==========================================
# Base
# ==========================================

class ShiftSlotBase(BaseModel):
    start_at: datetime
    end_at: datetime

    required_staff_count: int = Field(
        default=1,
        ge=1,
        description="必要人数（1以上）",
    )


    @model_validator(mode="after")
    def normalize_timezone(self):
        if self.start_at.tzinfo is None:
            self.start_at = self.start_at.replace(tzinfo=timezone.utc)

        if self.end_at.tzinfo is None:
            self.end_at = self.end_at.replace(tzinfo=timezone.utc)

        return self

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


# ==========================================
# Response
# ==========================================

class ShiftSlotResponse(ShiftSlotBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


