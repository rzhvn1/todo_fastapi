from fastapi import APIRouter

from api.v1.routes import users, tasks

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users")
api_router.include_router(tasks.router, prefix="/tasks")
