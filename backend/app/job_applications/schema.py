from pydantic import BaseModel, ConfigDict
from datetime import datetime

# 作成用
class JobApplicationCreate(BaseModel):
    organization_id: int
    job_title: str
   

# レスポンス用
class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    organization_id: int
    job_title: str
    organization_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)