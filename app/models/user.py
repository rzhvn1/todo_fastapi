from __future__ import annotations

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from db.database import Base

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
	username: Mapped[str] = mapped_column(String, nullable=True, unique=True, default=None)
	first_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
	last_name: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
	password: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

	def __repr__(self):
		return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"
	
	@staticmethod
	def get_by_email(session: Session, email: str) -> User | None:
		return session.scalar(select(User).where(User.email == email))
	
	@staticmethod
	def get_by_username(session: Session, username: str) -> User | None:
		return session.scalar(select(User).where(User.username == username))

