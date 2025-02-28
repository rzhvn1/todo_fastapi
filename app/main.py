from fastapi import FastAPI
from db.database import lifespan
from api.v1.routes.users import router as users_router

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)