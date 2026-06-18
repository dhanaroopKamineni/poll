"""Poll CRUD operations."""

from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Poll, PollOption, PollVote
from ..schemas.polls import PollCreate, PollUpdate, PollVoteCreate


def create_poll(db: Session, payload: PollCreate):
    """Create a new poll with options."""
    poll = Poll(
        title=payload.title,
        description=payload.description,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
    )

    db.add(poll)
    db.flush()

    for option in payload.options:
        db.add(
            PollOption(
                poll_id=poll.id,
                option_text=option.option_text
            )
        )

    db.commit()
    db.refresh(poll)

    return poll


def get_poll(db: Session, poll_id: int):
    """Get a poll by ID."""
    return db.query(Poll).filter(Poll.id == poll_id).first()


def get_active_poll(db: Session, poll_id: int, now: datetime | None = None):
    """Get a poll only if it is currently active."""
    now = now or datetime.utcnow()
    return (
        db.query(Poll)
        .filter(Poll.id == poll_id)
        .filter(Poll.start_datetime <= now)
        .filter(Poll.end_datetime >= now)
        .first()
    )


def get_active_polls(db: Session, now: datetime | None = None):
    """Get all polls currently available to users."""
    now = now or datetime.utcnow()
    return (
        db.query(Poll)
        .filter(Poll.start_datetime <= now)
        .filter(Poll.end_datetime >= now)
        .all()
    )


def update_poll(db: Session, poll_id: int, payload: PollUpdate):
    """Update a poll."""
    poll = get_poll(db, poll_id)
    if not poll:
        return None

    if payload.title is not None:
        poll.title = payload.title

    if payload.description is not None:
        poll.description = payload.description

    if payload.start_datetime is not None:
        poll.start_datetime = payload.start_datetime

    if payload.end_datetime is not None:
        poll.end_datetime = payload.end_datetime

    if payload.options is not None:
        poll.options.clear()
        db.flush()
        for option in payload.options:
            db.add(
                PollOption(
                    poll_id=poll.id,
                    option_text=option.option_text
                )
            )

    db.commit()
    db.refresh(poll)
    return poll


def delete_poll(db: Session, poll_id: int):
    """Delete a poll."""
    poll = get_poll(db, poll_id)
    if not poll:
        return False
    db.delete(poll)
    db.commit()
    return True


def vote_poll(db: Session, poll_id: int, payload: PollVoteCreate, voter_id: str):
    """Record a vote on a poll option by an authenticated user."""
    poll = get_poll(db, poll_id)
    now = datetime.utcnow()
    if not poll or poll.start_datetime > now or poll.end_datetime < now:
        return None

    vote = PollVote(
        poll_id=poll_id,
        option_id=payload.option_id,
        voter_id=voter_id
    )

    db.add(vote)
    db.commit()

    return vote


def get_poll_votes(db: Session):
    """Get all poll votes."""
    return db.query(PollVote).all()
