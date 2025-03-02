from fastapi import APIRouter
from schemas.task import TaskResponse, TaskCreate
from dependencies.db import SessionDep
from dependencies.user import CurrentUser
from models.task import Task


router = APIRouter()

@router.post("/", tags=["tasks"], response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    task_dict = task_in.model_dump()
    task = Task(owner_id=current_user.id, **task_dict)
    session.add(task)
    session.commit()
    session.refresh(task)

    return task

