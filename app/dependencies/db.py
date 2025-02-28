from typing import Annotated

from fastapi import Depends
from collections.abc import Generator
from sqlalchemy import exc
from sqlalchemy.orm import Session, sessionmaker
from db.database import engine


def get_session():
    with Session(engine) as session:
        yield session
            
SessionDep = Annotated[Session, Depends(get_session)]