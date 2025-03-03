from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from models.user import User
from db.database import Base



class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped[User] = relationship("User", back_populates="tasks")

    def __repr__(self): 
        return f"Task(id={self.id!r}, title={self.title!r})"
    