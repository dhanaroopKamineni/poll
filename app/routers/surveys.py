"""Survey management routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user, get_current_admin
from ..database import get_db
from ..crud.surveys import (
    create_survey,
    get_survey,
    get_surveys,
    update_survey,
    delete_survey,
    submit_survey,
)
from ..schemas.surveys import (
    SurveyCreate,
    SurveyResponse,
    SurveyUpdate,
    SurveySubmissionCreate,
    SurveySubmissionResponse,
)

router = APIRouter(prefix="/api/surveys", tags=["surveys"])


@router.post("", response_model=SurveyResponse)
def create_survey_api(
    payload: SurveyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Create a new survey (admin only)."""
    return create_survey(db, payload)


@router.get("", response_model=list[SurveyResponse])
def list_surveys(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get all surveys."""
    return get_surveys(db)


@router.get("/{survey_id}", response_model=SurveyResponse)
def get_survey_api(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get a survey by ID."""
    survey = get_survey(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


@router.put("/{survey_id}", response_model=SurveyResponse)
def update_survey_api(
    survey_id: int,
    payload: SurveyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Update a survey (admin only)."""
    survey = update_survey(db, survey_id, payload)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


@router.delete("/{survey_id}")
def delete_survey_api(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Delete a survey (admin only)."""
    deleted = delete_survey(db, survey_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Deleted successfully"}


@router.post("/submit", response_model=SurveySubmissionResponse)
def submit_survey_api(
    payload: SurveySubmissionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Submit a survey response (authenticated users only).
    
    The submitter is automatically recorded as the authenticated user.
    """
    return submit_survey(db, payload, current_user.username)
