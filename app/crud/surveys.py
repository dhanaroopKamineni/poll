"""Survey CRUD operations."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models import Survey, Question, Option, SurveySubmission, Answer, SurveySession
from ..schemas.surveys import SurveyCreate, SurveySubmissionCreate


def create_survey(db: Session, survey_data: SurveyCreate):
    """Create a new survey with questions and options."""
    survey = Survey(
        title=survey_data.title,
        description=survey_data.description,
        start_datetime=survey_data.start_datetime,
        end_datetime=survey_data.end_datetime,
    )

    db.add(survey)
    db.flush()

    for q in survey_data.questions:
        question = Question(
            survey_id=survey.id,
            question_text=q.question_text,
            question_type=q.question_type.value
        )

        db.add(question)
        db.flush()

        if q.question_type.value == "mcq":
            for opt in q.options:
                db.add(
                    Option(
                        question_id=question.id,
                        option_text=opt.option_text
                    )
                )

    db.commit()
    db.refresh(survey)

    return survey


def get_survey(db: Session, survey_id: int):
    """Get a survey by ID."""
    return (
        db.query(Survey)
        .filter(Survey.id == survey_id)
        .first()
    )


def get_active_surveys(db: Session, now: datetime | None = None):
    """Get all surveys currently available to users."""
    now = now or datetime.utcnow()
    return (
        db.query(Survey)
        .filter(Survey.start_datetime <= now)
        .filter(Survey.end_datetime >= now)
        .all()
    )


def get_survey_if_active(db: Session, survey_id: int, now: datetime | None = None):
    """Get a survey only if it is currently active."""
    now = now or datetime.utcnow()
    return (
        db.query(Survey)
        .filter(Survey.id == survey_id)
        .filter(Survey.start_datetime <= now)
        .filter(Survey.end_datetime >= now)
        .first()
    )


def update_survey(db: Session, survey_id: int, payload):
    """Update a survey."""
    survey = get_survey(db, survey_id)

    if not survey:
        return None

    if payload.title is not None:
        survey.title = payload.title

    if payload.description is not None:
        survey.description = payload.description

    if payload.start_datetime is not None:
        survey.start_datetime = payload.start_datetime

    if payload.end_datetime is not None:
        survey.end_datetime = payload.end_datetime

    db.commit()
    db.refresh(survey)

    return survey


def delete_survey(db: Session, survey_id: int):
    """Delete a survey."""
    survey = get_survey(db, survey_id)

    if not survey:
        return False

    db.delete(survey)
    db.commit()

    return True


def submit_survey(db: Session, payload: SurveySubmissionCreate, submitted_by: str):
    """Submit a survey response by an authenticated user."""
    response = SurveySubmission(
        survey_id=payload.survey_id,
        session_id=payload.session_id,
        submitted_by=submitted_by
    )

    db.add(response)
    db.flush()

    for ans in payload.answers:
        answer = Answer(
            response_id=response.id,
            question_id=ans.question_id,
            selected_option_id=ans.selected_option_id,
            answer_text=ans.answer_text
        )
        db.add(answer)

    session = db.query(SurveySession).filter(SurveySession.id == payload.session_id).first()
    if session:
        session.completed = True

    db.commit()
    db.refresh(response)

    return response


def get_survey_submissions(db: Session):
    """Get all survey submissions."""
    return db.query(SurveySubmission).all()


def start_survey_session(db: Session, survey_id: int, started_by: str):
    """Start a survey session and return the session object."""
    now = datetime.utcnow()
    expires = now + timedelta(minutes=10)
    session = SurveySession(
        survey_id=survey_id,
        started_by=started_by,
        started_at=now,
        expires_at=expires,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_survey_session(db: Session, session_id: int):
    """Return a survey session by ID."""
    return db.query(SurveySession).filter(SurveySession.id == session_id).first()


def validate_survey_session(db: Session, session_id: int, started_by: str):
    """Validate a survey session's time window and ownership."""
    now = datetime.utcnow()
    session = get_survey_session(db, session_id)
    if not session:
        return None
    if session.started_by != started_by:
        return None
    if session.completed:
        return None
    if session.expires_at < now:
        return None
    return session
