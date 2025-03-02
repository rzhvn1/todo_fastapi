from datetime import timedelta

from fastapi import (
	APIRouter,
	Depends,
	HTTPException,
	status
)
from sqlalchemy.exc import IntegrityError
from models.user import User
from schemas.user import Token
from schemas.user import UserLogin, UserRegister, UserResponse
from dependencies.db import SessionDep
from core.security import create_access_token, hash_password
from services.user_services import authenticate
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", tags=["auth"], response_model=UserResponse)
async def register_user(
	user: UserRegister,
	session: SessionDep,
):	
	existing_user = session.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

	if existing_user:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or username already exists")
	
	if not user.password:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
	
	if user.password != user.confirm_password:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords does not match")
	
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
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
	

@router.post("/login", tags=["auth"])
async def login(
	user: UserLogin,
	session: SessionDep,
) -> Token:
	user = authenticate(session=session, email=user.email, password=user.password)

	if not user:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrent email or password")
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

	return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

	


	
