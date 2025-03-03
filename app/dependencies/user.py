import jwt

from fastapi import Depends, HTTPException, status
from typing import Annotated
from models.user import User
from fastapi.security import OAuth2PasswordBearer
from dependencies.db import SessionDep
from models.user import User
from core.config import SECRET_KEY
from core.security import ALGORITHM
from schemas.user import TokenPayload
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/users/login"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

#ToDo: check the try section
def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]