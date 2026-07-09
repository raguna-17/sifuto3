from pydantic import BaseModel, ConfigDict


class SchedulerConfirmRequest(BaseModel):
    assignments: dict[int, list[int]]


class SchedulerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    assignments: dict[int, list[int]]