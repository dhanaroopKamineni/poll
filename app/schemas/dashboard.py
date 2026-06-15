"""Dashboard-related Pydantic schemas."""

from typing import List
from pydantic import BaseModel
from .surveys import SurveySubmissionDashboardResponse
from .polls import PollVoteResponse


class DashboardResponse(BaseModel):
    """Admin dashboard response model."""
    survey_submissions: List[SurveySubmissionDashboardResponse]
    poll_votes: List[PollVoteResponse]
