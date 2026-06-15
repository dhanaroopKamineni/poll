"""Routers package initialization."""

from .users import router as users_router
from .surveys import router as surveys_router
from .polls import router as polls_router
from .admin import router as admin_router

__all__ = [
    "users_router",
    "surveys_router",
    "polls_router",
    "admin_router",
]
