#!/usr/bin/env python3
"""Test survey workflow with session management."""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc4MTc2MzkwNn0.xdmBdZmL2HXgIe4UUv6rsaeezNpYco10h6b1JV5Wzgw"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_list_surveys():
    """Test listing active surveys."""
    print("\n1️⃣ List Active Surveys")
    resp = requests.get(f"{BASE_URL}/api/surveys", headers=headers)
    print(f"  Status: {resp.status_code}")
    surveys = resp.json()
    print(f"  Found {len(surveys)} surveys")
    if surveys:
        for s in surveys:
            print(f"    - {s['title']} (ID: {s['id']})")
    return surveys[0] if surveys else None


def test_start_session(survey_id):
    """Test starting a survey session."""
    print("\n2️⃣ Start Survey Session")
    payload = {"survey_id": survey_id}
    resp = requests.post(
        f"{BASE_URL}/api/surveys/sessions",
        headers=headers,
        json=payload
    )
    print(f"  Status: {resp.status_code}")
    session = resp.json()
    print(f"  Session ID: {session['id']}")
    print(f"  Expires At: {session['expires_at']}")
    return session


def test_submit_survey(survey_id, session_id):
    """Test submitting survey response."""
    print("\n3️⃣ Submit Survey Response")
    payload = {
        "survey_id": survey_id,
        "session_id": session_id,
        "answers": [
            {
                "question_id": 1,
                "selected_option_id": 1
            },
            {
                "question_id": 2,
                "answer_text": "Great service!"
            }
        ]
    }
    resp = requests.post(
        f"{BASE_URL}/api/surveys/submit",
        headers=headers,
        json=payload
    )
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        submission = resp.json()
        print(f"  Submission ID: {submission['id']}")
        print(f"  Submitted By: {submission['submitted_by']}")
        print(f"  Answers: {len(submission['answers'])}")
    else:
        print(f"  Error: {resp.json()}")


def test_poll_workflow():
    """Test poll creation and voting."""
    print("\n4️⃣ Create Poll")
    poll_payload = {
        "title": "Best Framework",
        "description": "What's your favorite web framework?",
        "options": [
            {"option_text": "FastAPI"},
            {"option_text": "Django"},
            {"option_text": "Flask"}
        ],
        "start_datetime": datetime.utcnow().isoformat(),
        "end_datetime": (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }
    resp = requests.post(
        f"{BASE_URL}/api/polls",
        headers=headers,
        json=poll_payload
    )
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        poll = resp.json()
        print(f"  Poll ID: {poll['id']}")
        return poll
    else:
        print(f"  Error: {resp.json()}")
    return None


def test_vote_poll(poll_id):
    """Test voting on poll."""
    if not poll_id:
        return
    print("\n5️⃣ Vote on Poll")
    payload = {"option_id": 1}
    resp = requests.post(
        f"{BASE_URL}/api/polls/{poll_id}/vote",
        headers=headers,
        json=payload
    )
    print(f"  Status: {resp.status_code}")
    print(f"  Response: {resp.json()}")


if __name__ == "__main__":
    print("=" * 50)
    print("Survey & Poll API Workflow Test")
    print("=" * 50)
    
    survey = test_list_surveys()
    if survey:
        session = test_start_session(survey["id"])
        test_submit_survey(survey["id"], session["id"])
    
    poll = test_poll_workflow()
    if poll:
        test_vote_poll(poll["id"])
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("=" * 50)
