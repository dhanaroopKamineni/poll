"""SQLAlchemy ORM models for surveys, polls, and users."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Enum
)
from sqlalchemy.orm import relationship

from .database import Base

QUESTION_TYPES = ("mcq", "text")
USER_ROLES = ("user", "admin")


class User(Base):
    """User model with authentication credentials and role."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        Enum(*USER_ROLES, name="user_role"),
        nullable=False,
        default="user"
    )


class Survey(Base):
    """Survey model with questions."""
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    questions = relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan"
    )
    responses = relationship(
        "SurveySubmission",
        back_populates="survey"
    )


class Question(Base):
    """Survey question model."""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(
        Integer,
        ForeignKey("surveys.id", ondelete="CASCADE")
    )
    question_text = Column(Text, nullable=False)
    question_type = Column(
        Enum(*QUESTION_TYPES, name="question_type"),
        nullable=False
    )

    survey = relationship(
        "Survey",
        back_populates="questions"
    )

    options = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan"
    )


class Option(Base):
    """Multiple choice option for a question."""
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    option_text = Column(Text, nullable=False)

    question = relationship(
        "Question",
        back_populates="options"
    )


class SurveySubmission(Base):
    """Survey submission by a user."""
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True)
    survey_id = Column(
        Integer,
        ForeignKey("surveys.id", ondelete="CASCADE")
    )
    submitted_by = Column(String(100), nullable=False)

    survey = relationship(
        "Survey",
        back_populates="responses"
    )

    answers = relationship(
        "Answer",
        back_populates="response",
        cascade="all, delete-orphan"
    )


class Answer(Base):
    """User's answer to a survey question."""
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    response_id = Column(
        Integer,
        ForeignKey("survey_responses.id", ondelete="CASCADE")
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )
    selected_option_id = Column(
        Integer,
        ForeignKey("options.id"),
        nullable=True
    )
    answer_text = Column(Text, nullable=True)

    response = relationship(
        "SurveySubmission",
        back_populates="answers"
    )


class Poll(Base):
    """Poll model with options."""
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    options = relationship(
        "PollOption",
        back_populates="poll",
        cascade="all, delete-orphan"
    )

    votes = relationship(
        "PollVote",
        back_populates="poll",
        cascade="all, delete-orphan"
    )


class PollOption(Base):
    """Poll option model."""
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True)
    poll_id = Column(
        Integer,
        ForeignKey("polls.id", ondelete="CASCADE")
    )
    option_text = Column(Text, nullable=False)

    poll = relationship(
        "Poll",
        back_populates="options"
    )


class PollVote(Base):
    """User vote on a poll option."""
    __tablename__ = "poll_votes"

    id = Column(Integer, primary_key=True)
    poll_id = Column(
        Integer,
        ForeignKey("polls.id", ondelete="CASCADE")
    )
    option_id = Column(
        Integer,
        ForeignKey("poll_options.id")
    )
    voter_id = Column(String(100), nullable=False)

    poll = relationship(
        "Poll",
        back_populates="votes"
    )
