from fastapi import FastAPI
from db.database import lifespan
from api.v1.routes.users import router as users_router
from api.v1.routes.tasks import router as tasks_router

app = FastAPI(
    lifespan=lifespan
)

app.include_router(users_router, prefix="/users")
app.include_router(tasks_router, prefix="/tasks")