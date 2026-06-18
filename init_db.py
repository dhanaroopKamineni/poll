#!/usr/bin/env python3
"""Database initialization script to set up schema with new datetime fields."""

import sys
from sqlalchemy import inspect
from app.database import Base, engine
from app.models import Survey, Poll, SurveySession


def check_table_columns(table_name, expected_columns):
    """Check if table has all expected columns."""
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        return False, "Table does not exist"
    
    actual_columns = {col["name"] for col in inspector.get_columns(table_name)}
    missing_columns = expected_columns - actual_columns
    
    if missing_columns:
        return False, f"Missing columns: {missing_columns}"
    return True, "OK"


def init_db():
    """Initialize database tables."""
    print("Checking database schema...")
    
    # Check surveys table
    survey_cols = {"id", "title", "description", "start_datetime", "end_datetime"}
    ok, msg = check_table_columns("surveys", survey_cols)
    print(f"  surveys: {msg}")
    
    # Check polls table
    poll_cols = {"id", "title", "description", "start_datetime", "end_datetime"}
    ok, msg = check_table_columns("polls", poll_cols)
    print(f"  polls: {msg}")
    
    # Check survey_sessions table
    session_ok = inspect(engine).has_table("survey_sessions")
    print(f"  survey_sessions: {'OK' if session_ok else 'Missing'}")
    
    # Recreate all tables
    print("\nRecreating tables with correct schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully!")
    
    # Verify
    print("\nVerifying schema...")
    inspector = inspect(engine)
    for table_name in ["surveys", "polls", "survey_sessions", "users"]:
        if inspector.has_table(table_name):
            columns = [col["name"] for col in inspector.get_columns(table_name)]
            print(f"  {table_name}: {', '.join(columns)}")


if __name__ == "__main__":
    try:
        init_db()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
