"""User CRUD operations."""

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models import User
from ..schemas.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, payload: UserCreate):
    """Create a new user with hashed password."""
    user = User(
        username=payload.username,
        hashed_password=pwd_context.hash(payload.password),
        role=payload.role or "user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
