#!/usr/bin/env python3
"""Create a test admin user for testing."""

from app.crud.users import create_user
from app.schemas.users import UserCreate
from app.database import SessionLocal


def create_test_admin():
    """Create a test admin user."""
    db = SessionLocal()
    try:
        payload = UserCreate(username="admin", password="admin123", role="admin")
        user = create_user(db, payload)
        print(f"✓ Created admin user: {user.username}")
        return user
    except Exception as e:
        print(f"✗ Error creating user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_admin()
