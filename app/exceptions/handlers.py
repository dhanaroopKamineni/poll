"""Custom exception handlers."""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Handle SQLAlchemy exceptions."""
        logger.error(f"Database error: {str(exc)}")
        detail = str(exc.__cause__) if exc.__cause__ else str(exc)
        return JSONResponse(
            status_code=500,
            content={"detail": detail if DEBUG_MODE else "Database error occurred"},
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}")
        detail = str(exc)
        return JSONResponse(
            status_code=500,
            content={"detail": detail if DEBUG_MODE else "Internal server error"},
        )
