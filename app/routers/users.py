"""User authentication and registration routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import authenticate_user, create_access_token, get_current_active_user
from ..database import get_db
from ..crud.users import get_user_by_username, create_user
from ..schemas.users import UserCreate, UserResponse, LoginRequest, Token

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = get_user_by_username(db, payload.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return create_user(db, payload)


@router.post("/token", response_model=Token)
def login_for_access_token(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT access token."""
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_active_user)):
    """Get current authenticated user information."""
    return current_user
