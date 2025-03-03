import uuid

from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None
    is_completed: bool = False
    owner_id: int | None = None



class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    is_completed: bool
    created_at: datetime
    updated_at: datetime | None


class TaskPublic(TaskBase):
    id: int
    owner_id: int | None

    class Config:
        from_attributes = True


class TasksPublic(BaseModel):
    data: list[TaskPublic]
    count: int