from fastapi import (
	APIRouter,
	Depends,
	HTTPException,
	status
)
from sqlalchemy.exc import IntegrityError
from models.user import User
from schemas.user import UserRegister, UserResponse
from dependencies.db import SessionDep
from utils.user import hash_password

router = APIRouter()

@router.post("/register", tags=["auth"], response_model=UserResponse)
async def register_user(
	user: UserRegister,
	session: SessionDep,
):	
	if User.get_by_email(session=session, email=user.email):
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
	
	if User.get_by_username(session=session, username=user.username):
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
	
	if not user.password:
		return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is required")
	
	if user.password != user.confirm_password:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords does not match")
	
	hashed_password = hash_password(user.password)
	try:
		new_user = User(
			email=user.email,
			username=user.username,
			first_name=user.first_name,
			last_name=user.last_name,
			password=hashed_password
		)
		session.add(new_user)
		session.commit()
		session.refresh(new_user)
		return new_user
	except IntegrityError:
		session.rollback()
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


	
