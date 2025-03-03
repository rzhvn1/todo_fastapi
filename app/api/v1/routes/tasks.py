from fastapi import APIRouter, HTTPException
from schemas.task import TaskResponse, TaskCreate
from dependencies.db import SessionDep
from dependencies.user import CurrentUser, TokenDep
from models.task import Task
from models.user import User


router = APIRouter()

@router.post("/", tags=["tasks"], response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskResponse:
    owner = session.get(User, task_in.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    task = Task(
        title=task_in.title,
        description=task_in.description,
        is_completed=task_in.is_completed,
        owner_id=owner.id
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return task

