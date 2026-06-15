"""Poll CRUD operations."""

from sqlalchemy.orm import Session

from ..models import Poll, PollOption, PollVote
from ..schemas.polls import PollCreate, PollVoteCreate


def create_poll(db: Session, payload: PollCreate):
    """Create a new poll with options."""
    poll = Poll(
        title=payload.title,
        description=payload.description
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


def get_polls(db: Session):
    """Get all polls."""
    return db.query(Poll).all()


def update_poll(db: Session, poll_id: int, payload: PollCreate):
    """Update a poll."""
    poll = get_poll(db, poll_id)
    if not poll:
        return None

    poll.title = payload.title
    poll.description = payload.description
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
