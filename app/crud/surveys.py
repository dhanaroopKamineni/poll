"""Survey CRUD operations."""

from sqlalchemy.orm import Session

from ..models import Survey, Question, Option, SurveySubmission, Answer
from ..schemas.surveys import SurveyCreate, SurveySubmissionCreate


def create_survey(db: Session, survey_data: SurveyCreate):
    """Create a new survey with questions and options."""
    survey = Survey(
        title=survey_data.title,
        description=survey_data.description
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


def get_surveys(db: Session):
    """Get all surveys."""
    return db.query(Survey).all()


def update_survey(db: Session, survey_id: int, payload):
    """Update a survey."""
    survey = get_survey(db, survey_id)

    if not survey:
        return None

    if payload.title is not None:
        survey.title = payload.title

    if payload.description is not None:
        survey.description = payload.description

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

    db.commit()
    db.refresh(response)

    return response


def get_survey_submissions(db: Session):
    """Get all survey submissions."""
    return db.query(SurveySubmission).all()
