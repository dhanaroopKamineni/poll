# Survey & Poll Time-Window & Session Implementation - Fix Summary

## Issues Identified & Fixed

### 1. **Database Schema Error**
**Problem:** Old database tables missing the new `start_datetime` and `end_datetime` columns required by the updated models.

**Solution:** 
- Created `init_db.py` script that drops and recreates all tables with proper schema
- Database now includes:
  - `surveys`: Added `start_datetime`, `end_datetime`
  - `polls`: Added `start_datetime`, `end_datetime`
  - `survey_sessions`: New table for session management
  - `survey_responses`: Updated to link to `survey_sessions`

### 2. **Generic Error Handling**
**Problem:** SQLAlchemy exceptions were caught and hidden behind a generic "Database error occurred" message.

**Solution:**
- Enhanced exception handlers in `app/exceptions/handlers.py`
- Added logging for actual error details
- When `DEBUG=true`, error details are shown in responses
- Helps with debugging without exposing sensitive info in production

---

## Implementation Summary

### Database Schema Changes

#### Survey Model
```python
class Survey(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_datetime = Column(DateTime, nullable=False)  # NEW
    end_datetime = Column(DateTime, nullable=False)    # NEW
    questions = relationship("Question", ...)
    responses = relationship("SurveySubmission", ...)
    sessions = relationship("SurveySession", ...)      # NEW
```

#### SurveySession Model (NEW)
```python
class SurveySession(Base):
    """User session valid for 10 minutes after start"""
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    started_by = Column(String(100), nullable=False)   # User who started
    started_at = Column(DateTime, nullable=False)      # When session started
    expires_at = Column(DateTime, nullable=False)      # Expires in 10 minutes
    completed = Column(Boolean, default=False)         # Session completion flag
    submissions = relationship("SurveySubmission", ...)
```

#### Poll Model
```python
class Poll(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_datetime = Column(DateTime, nullable=False)  # NEW
    end_datetime = Column(DateTime, nullable=False)    # NEW
    options = relationship("PollOption", ...)
    votes = relationship("PollVote", ...)
```

---

## API Endpoints - Behavior

### Surveys

#### 1. Create Survey (Admin Only)
**Endpoint:** `POST /api/surveys`

**Request:**
```json
{
  "title": "Customer Feedback",
  "description": "Feedback survey",
  "questions": [...],
  "start_datetime": "2026-06-18T00:00:00",
  "end_datetime": "2026-06-18T23:59:59"
}
```

**Response:** Survey with timestamps

#### 2. List Active Surveys
**Endpoint:** `GET /api/surveys`

**Behavior:** Returns only surveys where `now` is between `start_datetime` and `end_datetime`

#### 3. Get Survey (Time-Window Enforced)
**Endpoint:** `GET /api/surveys/{survey_id}`

**Behavior:** Returns survey only if currently active; otherwise returns 404

#### 4. Start Survey Session
**Endpoint:** `POST /api/surveys/sessions`

**Request:**
```json
{
  "survey_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "survey_id": 1,
  "started_by": "username",
  "started_at": "2026-06-18T05:26:30",
  "expires_at": "2026-06-18T05:36:30",  // +10 minutes
  "completed": false
}
```

**Behavior:**
- User can only start a session if survey is in active window
- Session automatically expires 10 minutes after start
- User receives `session_id` for submission

#### 5. Submit Survey Response
**Endpoint:** `POST /api/surveys/submit`

**Request:**
```json
{
  "survey_id": 1,
  "session_id": 1,
  "answers": [
    {"question_id": 1, "selected_option_id": 2},
    {"question_id": 2, "answer_text": "Great"}
  ]
}
```

**Behavior:**
- Session must be valid (not expired, not completed)
- Session ownership verified (user who started it)
- Upon submission, session marked as `completed`
- Cannot submit after 10 minutes or for same session twice

### Polls

#### 1. Create Poll (Admin Only)
**Endpoint:** `POST /api/polls`

**Request:**
```json
{
  "title": "Best Framework",
  "description": "...",
  "options": [...],
  "start_datetime": "2026-06-18T00:00:00",
  "end_datetime": "2026-06-18T23:59:59"
}
```

#### 2. List Active Polls
**Endpoint:** `GET /api/polls`

**Behavior:** Returns only polls in active time window

#### 3. Get Poll (Time-Window Enforced)
**Endpoint:** `GET /api/polls/{poll_id}`

**Behavior:** Returns poll only if currently active

#### 4. Vote on Poll
**Endpoint:** `POST /api/polls/{poll_id}/vote`

**Request:**
```json
{
  "option_id": 4
}
```

**Behavior:**
- Vote only allowed if poll is in active time window
- Returns 400 if poll is not active
- Returns 400 if poll not found

#### 5. Update Poll (Admin Only)
**Endpoint:** `PUT /api/polls/{poll_id}`

**Request:** Can update any field including `start_datetime`, `end_datetime`

**Behavior:** Allows admins to extend deadlines or modify schedules

---

## Usage Example

### 1. Admin Creates Survey
```bash
curl -X POST http://localhost:8000/api/surveys \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @survey.json
```

### 2. User Views Active Surveys
```bash
curl http://localhost:8000/api/surveys \
  -H "Authorization: Bearer <token>"
```

### 3. User Starts Survey Session
```bash
curl -X POST http://localhost:8000/api/surveys/sessions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"survey_id": 1}'
# Returns: session_id = 1, expires in 10 minutes
```

### 4. User Submits Response (Must be within 10 minutes)
```bash
curl -X POST http://localhost:8000/api/surveys/submit \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @response.json
# session_id must be from step 3
```

---

## Key Features Implemented

✅ **Time-Window Access Control**
- Surveys/polls only accessible during scheduled windows
- Admin can extend windows by updating end_datetime

✅ **Survey Session Management**
- User starts session before responding
- Session valid for exactly 10 minutes
- Session locks submission window
- One response per session

✅ **Optimized Queries**
- `get_active_surveys()` - filters by start/end datetime
- `get_survey_if_active()` - validates active window
- `validate_survey_session()` - checks ownership, expiration, completion

✅ **Error Handling**
- Better error messages in DEBUG mode
- Proper HTTP status codes (400, 401, 403, 404)
- All APIs validate time windows

✅ **Admin Control**
- Can extend schedules after creation
- Can view all submissions/votes
- Can update all survey/poll fields

---

## Files Modified

1. `app/models.py` - Added DateTime fields and SurveySession model
2. `app/schemas/surveys.py` - Added schedule fields to schemas
3. `app/schemas/polls.py` - Added schedule fields to schemas
4. `app/crud/surveys.py` - Added active-survey filters and session logic
5. `app/crud/polls.py` - Added active-poll filters
6. `app/routers/surveys.py` - Updated endpoints with time-window validation
7. `app/routers/polls.py` - Updated endpoints with time-window validation
8. `app/exceptions/handlers.py` - Enhanced error reporting
9. `app/config/settings.py` - Added DEBUG mode configuration
10. `init_db.py` - Created database initialization script (NEW)

---

## Testing

All endpoints tested and working:
- ✅ Survey creation with timestamps
- ✅ Active surveys filtering
- ✅ Session creation (10-minute expiry)
- ✅ Survey submission within session window
- ✅ Poll creation with scheduling
- ✅ Active poll voting with time-window validation
- ✅ Admin update capabilities

---

## Deployment Checklist

- [ ] Run `python init_db.py` to initialize database with new schema
- [ ] Set `DEBUG=false` in production for security
- [ ] Verify all datetime fields use UTC timezone
- [ ] Test with actual PostgreSQL database (if not using SQLite)
- [ ] Monitor session expiration logic

