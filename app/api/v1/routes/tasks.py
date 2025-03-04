from typing import Any
from fastapi import APIRouter, HTTPException, status
from schemas.task import TaskPublic, TaskCreateUpdate, TasksPublic
from dependencies.db import SessionDep
from dependencies.user import CurrentUser
from models.task import Task
from models.user import User
from sqlalchemy import select, func


router = APIRouter()

@router.get("/", tags=["tasks"], response_model=TasksPublic)
async def get_tasks(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0, 
    limit: int = 100,
    owner_id: int | None = None,
) -> Any:
    if owner_id:
        owner = session.get(User, owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        count_statement = (
            select(func.count())
            .select_from(Task)
            .where(Task.owner_id == owner.id)
        )
        count = session.execute(count_statement).scalars().one()
        statement = (
            select(Task)
            .where(Task.owner_id == owner.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.execute(statement).scalars().all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Task)
        )
        count = session.execute(count_statement).scalars().one()
        statement = (
            select(Task)
            .offset(skip)
            .limit(limit)
        )
        items = session.execute(statement).scalars().all()
    

    return TasksPublic(data=items, count=count)

@router.get("/{id}", tags=["tasks"], response_model=TaskPublic)
async def get_task(
    session: SessionDep,
    current_user: CurrentUser,
    id: int
) -> Any:
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/", tags=["tasks"], response_model=TaskPublic)
async def create_task(
    task_in: TaskCreateUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> TaskPublic:
    if task_in.owner_id:
        owner = session.get(User, task_in.owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    task = Task(
        title=task_in.title,
        description=task_in.description,
        is_completed=task_in.is_completed,
        owner_id=task_in.owner_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.put("/{id}", tags=["tasks"], response_model=TaskPublic)
async def update_task(
    task_in: TaskCreateUpdate,
    session: SessionDep,
    current_user: CurrentUser,
    id: int
) -> Any:
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_dict = task_in.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
