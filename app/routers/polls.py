"""Poll management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user, get_current_admin
from ..database import get_db
from ..crud.polls import (
    create_poll,
    get_poll,
    get_active_poll,
    get_active_polls,
    update_poll,
    delete_poll,
    vote_poll,
)
from ..schemas.polls import (
    PollCreate,
    PollUpdate,
    PollResponse,
    PollVoteCreate,
)

router = APIRouter(prefix="/api/polls", tags=["polls"])


@router.post("", response_model=PollResponse)
def create_poll_api(
    payload: PollCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Create a new poll (admin only)."""
    return create_poll(db, payload)


@router.get("", response_model=list[PollResponse])
def list_polls(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get active polls currently available to the authenticated user."""
    return get_active_polls(db)


@router.get("/{poll_id}", response_model=PollResponse)
def get_poll_api(
    poll_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get an active poll by ID."""
    poll = get_active_poll(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found or not active")
    return poll


@router.put("/{poll_id}", response_model=PollResponse)
def update_poll_api(
    poll_id: int,
    payload: PollUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Update a poll (admin only)."""
    poll = update_poll(db, poll_id, payload)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll


@router.delete("/{poll_id}")
def delete_poll_api(
    poll_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Delete a poll (admin only)."""
    deleted = delete_poll(db, poll_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Poll not found")
    return {"message": "Deleted successfully"}


@router.post("/{poll_id}/vote")
def vote_poll_api(
    poll_id: int,
    payload: PollVoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Vote on a poll option (authenticated users only).
    
    The voter is automatically recorded as the authenticated user.
    """
    vote = vote_poll(db, poll_id, payload, current_user.username)
    if not vote:
        raise HTTPException(status_code=400, detail="Poll not found or not active")
    return {"message": "Vote recorded"}
