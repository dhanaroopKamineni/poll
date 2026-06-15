"""User-related Pydantic schemas."""

from typing import Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    """Token data model."""
    username: Optional[str] = None
    role: Optional[str] = None


class UserBase(BaseModel):
    """Base user model."""
    username: str
    role: str | None = "user"


class UserCreate(UserBase):
    """User creation model."""
    password: str

    class Config:
        extra = "ignore"


class UserResponse(UserBase):
    """User response model."""
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str
