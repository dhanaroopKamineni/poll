"""Admin dashboard routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.security import get_current_admin
from ..database import get_db
from ..crud.surveys import get_survey_submissions
from ..crud.polls import get_poll_votes
from ..schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard", response_model=DashboardResponse)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    """Get admin dashboard with all survey submissions and poll votes (admin only)."""
    survey_submissions = get_survey_submissions(db)
    poll_votes = get_poll_votes(db)
    return {
        "survey_submissions": survey_submissions,
        "poll_votes": poll_votes
    }
