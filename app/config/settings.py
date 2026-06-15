"""Application configuration settings."""

import os
from functools import lru_cache


class Settings:
    """Application settings."""
    
    # Application
    APP_NAME: str = "Poll API"
    APP_DESCRIPTION: str = "A survey and polling system with JWT authentication and role-based access control"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/poll"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY_POLL_APP")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()
