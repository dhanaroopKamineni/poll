"""Survey and question-related Pydantic schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class QuestionType(str, Enum):
    """Question type enumeration."""
    mcq = "mcq"
    text = "text"


class OptionBase(BaseModel):
    """Base option model."""
    option_text: str


class OptionCreate(OptionBase):
    """Option creation model."""
    pass


class OptionResponse(OptionBase):
    """Option response model."""
    id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    """Base question model."""
    question_text: str
    question_type: QuestionType


class QuestionCreate(QuestionBase):
    """Question creation model."""
    options: Optional[List[OptionCreate]] = []


class QuestionUpdate(BaseModel):
    """Question update model."""
    question_text: Optional[str] = None
    question_type: Optional[QuestionType] = None


class QuestionResponse(QuestionBase):
    """Question response model."""
    id: int
    options: List[OptionResponse] = []

    class Config:
        from_attributes = True


class SurveyBase(BaseModel):
    """Base survey model."""
    title: str
    description: Optional[str] = None


class SurveyCreate(SurveyBase):
    """Survey creation model."""
    questions: Optional[List[QuestionCreate]] = []
    start_datetime: datetime
    end_datetime: datetime


class SurveyUpdate(BaseModel):
    """Survey update model."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None


class SurveyResponse(SurveyBase):
    """Survey response model."""
    id: int
    questions: List[QuestionResponse] = []
    start_datetime: datetime
    end_datetime: datetime

    class Config:
        from_attributes = True


class AnswerCreate(BaseModel):
    """Answer creation model."""
    question_id: int
    selected_option_id: Optional[int] = None
    answer_text: Optional[str] = None


class SurveySessionStartRequest(BaseModel):
    """Request to start a survey session."""
    survey_id: int


class SurveySubmissionCreate(BaseModel):
    """Survey submission creation model."""
    survey_id: int
    session_id: int
    answers: List[AnswerCreate]


class AnswerResponse(BaseModel):
    """Answer response model."""
    id: int
    question_id: int
    selected_option_id: Optional[int]
    answer_text: Optional[str]

    class Config:
        from_attributes = True


class SurveySessionResponse(BaseModel):
    """Survey session response model."""
    id: int
    survey_id: int
    started_by: str
    started_at: datetime
    expires_at: datetime
    completed: bool

    class Config:
        from_attributes = True


class SurveySubmissionResponse(BaseModel):
    """Survey submission response model."""
    id: int
    survey_id: int
    session_id: int
    submitted_by: str
    answers: List[AnswerResponse]

    class Config:
        from_attributes = True


class SurveySubmissionDashboardResponse(BaseModel):
    """Survey submission dashboard response model."""
    id: int
    survey_id: int
    submitted_by: str
    answers: List[AnswerResponse]

    class Config:
        from_attributes = True
