from sqlalchemy.orm import Session
from core.security import verify_password
from models.user import User

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = User.get_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user