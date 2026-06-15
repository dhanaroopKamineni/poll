"""Poll Application - Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import get_settings
from .database import Base, engine
from .routers import users_router, surveys_router, polls_router, admin_router
from .exceptions import register_exception_handlers

# Create database tables
Base.metadata.create_all(bind=engine)

# Get settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(users_router)
app.include_router(surveys_router)
app.include_router(polls_router)
app.include_router(admin_router)


@app.get("/", tags=["root"])
def read_root():
    """Welcome endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "version": settings.APP_VERSION
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
