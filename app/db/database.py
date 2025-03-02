import os

from fastapi import FastAPI
from sqlmodel import create_engine
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

print(os.getenv("DATABASE_URL"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
if DATABASE_URL == "":
    DATABASE_URL = "sqlite:///db.sqlite"


engine = create_engine(
    DATABASE_URL,
    echo=True
)

class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def lifespan(application: FastAPI):
    if os.getenv("APP_ENV") != "PROD":
        with engine.begin() as conn:
            print("CHET MA")
            Base.metadata.create_all(conn)
            print("HAHHA")

    yield