"""Utility functions."""

from typing import Any, Dict
from fastapi import HTTPException, status


def raise_http_exception(
    status_code: int,
    detail: str,
    headers: Dict[str, Any] | None = None
) -> None:
    """Raise an HTTP exception."""
    raise HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )


def raise_not_found(detail: str = "Resource not found") -> None:
    """Raise 404 Not Found exception."""
    raise_http_exception(status.HTTP_404_NOT_FOUND, detail)


def raise_unauthorized(detail: str = "Unauthorized") -> None:
    """Raise 401 Unauthorized exception."""
    raise_http_exception(
        status.HTTP_401_UNAUTHORIZED,
        detail,
        {"WWW-Authenticate": "Bearer"}
    )


def raise_forbidden(detail: str = "Access forbidden") -> None:
    """Raise 403 Forbidden exception."""
    raise_http_exception(status.HTTP_403_FORBIDDEN, detail)


def raise_bad_request(detail: str) -> None:
    """Raise 400 Bad Request exception."""
    raise_http_exception(status.HTTP_400_BAD_REQUEST, detail)
