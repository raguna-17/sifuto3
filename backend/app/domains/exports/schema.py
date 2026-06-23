from pydantic import BaseModel, ConfigDict


class ShiftExportRow(BaseModel):
    """
    1行分のシフト出力データ
    """

    model_config = ConfigDict(from_attributes=True)

    date: str
    slot_id: int

    user_id: int
    user_name: str

    is_auto: bool
    is_confirmed: bool

    required_staff_count: int