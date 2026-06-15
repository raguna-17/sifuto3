from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator

from app.core.enums import PreferencePriority


# =========================
# base
# =========================
class ShiftPreferenceBase(BaseModel):
    target_date: date
    shift_slot_id: int

    start_at: datetime | None = None
    end_at: datetime | None = None

    priority: PreferencePriority = PreferencePriority.NEUTRAL
    note: str | None = None

    @model_validator(mode="after")
    def validate_time_range(self):
        # ① 両方 or 両方None を保証
        if (self.start_at is None) != (self.end_at is None):
            raise ValueError(
                "start_at and end_at must both be set or both be None"
            )

        # ② 両方ある場合のみ整合性チェック
        if self.start_at and self.end_at:
            if self.start_at >= self.end_at:
                raise ValueError(
                    "start_at must be earlier than end_at"
                )

        return self


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

    @model_validator(mode="after")
    def validate_time_range(self):
        # updateはpartialなので「揃った時だけチェック」
        if self.start_at is not None and self.end_at is not None:
            if self.start_at >= self.end_at:
                raise ValueError(
                    "start_at must be earlier than end_at"
                )

        return self


# =========================
# response
# =========================
class ShiftPreferenceResponse(ShiftPreferenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int