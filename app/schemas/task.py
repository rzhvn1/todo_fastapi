from pydantic import BaseModel
from datetime import datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int

class TaskCreate(BaseModel):
    title: str
    description: str | None
    is_completed: bool | None
    owner_id: int