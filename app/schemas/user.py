from pydantic import BaseModel


class UserRegister(BaseModel):
	email: str
	username: str
	first_name: str | None
	last_name: str | None
	password: str
	confirm_password: str

class UserResponse(BaseModel):
	id: int
	email: str
	username: str
	first_name: str
	last_name: str
