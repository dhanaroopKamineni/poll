"""Poll-related Pydantic schemas."""

from typing import List
from pydantic import BaseModel


class PollOptionCreate(BaseModel):
    """Poll option creation model."""
    option_text: str


class PollCreate(BaseModel):
    """Poll creation model."""
    title: str
    description: str | None = None
    options: List[PollOptionCreate]


class PollVoteCreate(BaseModel):
    """Poll vote creation model."""
    option_id: int


class PollOptionResponse(BaseModel):
    """Poll option response model."""
    id: int
    option_text: str

    class Config:
        from_attributes = True


class PollResponse(BaseModel):
    """Poll response model."""
    id: int
    title: str
    description: str | None
    options: List[PollOptionResponse]

    class Config:
        from_attributes = True


class PollVoteResponse(BaseModel):
    """Poll vote response model."""
    id: int
    poll_id: int
    option_id: int
    voter_id: str

    class Config:
        from_attributes = True
