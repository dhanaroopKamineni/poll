# Project Architecture

## Overview

This poll application follows a layered architecture pattern with clean separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    API Routers                          │
│  (users, surveys, polls, admin)                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│         Request/Response Schemas (Pydantic)             │
│  (users, surveys, polls, dashboard)                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│            CRUD Operations Layer                        │
│  (users, surveys, polls)                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│         SQLAlchemy ORM Models                           │
│  (User, Survey, Question, Option, Poll, etc.)          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                        │
└─────────────────────────────────────────────────────────┘
```

## Module Breakdown

### `app/main.py`
- FastAPI application factory
- Route registration
- Middleware configuration
- Database initialization

### `app/auth.py`
- JWT token creation and validation
- Password hashing and verification
- Dependency injection for authentication
- Role-based authorization (user, admin)

### `app/database.py`
- SQLAlchemy engine and session configuration
- Database connection management
- Session dependency for FastAPI

### `app/models.py`
- SQLAlchemy ORM models
- Database schema definitions
- Relationships between entities
- Enums for roles and question types

### `app/schemas/`
**users.py**
- User authentication schemas
- Token models

**surveys.py**
- Survey CRUD schemas
- Question and option schemas
- Survey submission schemas

**polls.py**
- Poll CRUD schemas
- Poll option schemas
- Poll vote schemas

**dashboard.py**
- Admin dashboard response schema

### `app/crud/`
**users.py**
- User lookup by username
- User creation with password hashing

**surveys.py**
- Full CRUD for surveys
- Survey submission handling with automatic user attribution

**polls.py**
- Full CRUD for polls
- Vote recording with automatic user attribution

### `app/routers/`
**users.py**
- `/api/users` - Registration
- `/api/token` - Login
- `/api/me` - Get current user

**surveys.py**
- `/api/surveys` - CRUD operations
- `/api/surveys/submit` - Submit survey responses

**polls.py**
- `/api/polls` - CRUD operations
- `/api/polls/{id}/vote` - Vote on polls

**admin.py**
- `/api/admin/dashboard` - View all submissions and votes

## Authentication & Authorization Flow

```
User Request
    ↓
[HTTPBearer Token Extraction]
    ↓
[JWT Token Validation]
    ↓
[User Lookup in Database]
    ↓
[Role Check (if admin required)]
    ↓
[Route Handler Execution]
    ↓
[Response with User Attribution]
```

## Data Flow for Survey Submission

```
1. User (authenticated) sends POST /api/surveys/submit
        ↓
2. Router receives SurveySubmissionCreate payload
        ↓
3. Dependency extracts current_user from JWT token
        ↓
4. CRUD function receives:
   - payload (survey_id, answers)
   - submitted_by = current_user.username
        ↓
5. SurveySubmission created with submitted_by set
        ↓
6. Answers stored in database
        ↓
7. Response returned with all submission details
```

## Database Schema

### Users Table
- id (PK)
- username (UNIQUE)
- hashed_password
- role (ENUM: user, admin)

### Surveys Table
- id (PK)
- title
- description
- Relationships: questions, responses

### Questions Table
- id (PK)
- survey_id (FK)
- question_text
- question_type (ENUM: mcq, text)
- Relationships: options, answers

### Options Table
- id (PK)
- question_id (FK)
- option_text

### SurveySubmissions Table
- id (PK)
- survey_id (FK)
- submitted_by (username)
- Relationships: answers

### Answers Table
- id (PK)
- response_id (FK)
- question_id (FK)
- selected_option_id (FK)
- answer_text

### Polls Table
- id (PK)
- title
- description
- Relationships: options, votes

### PollOptions Table
- id (PK)
- poll_id (FK)
- option_text

### PollVotes Table
- id (PK)
- poll_id (FK)
- option_id (FK)
- voter_id (username)

## Key Design Decisions

1. **User Attribution**: Submissions and votes are tied to authenticated users via their username
2. **Role-Based Access**: Simple two-role system (user, admin) for easy management
3. **JWT Authentication**: Stateless authentication allows horizontal scaling
4. **Cascading Deletes**: Related data automatically deleted when parent is deleted
5. **Pydantic Schemas**: Automatic validation and documentation of request/response data
6. **Layered Architecture**: Clean separation between routing, business logic, and data access

## Error Handling

- **400 Bad Request**: Username already exists, invalid data
- **401 Unauthorized**: Invalid credentials or missing token
- **403 Forbidden**: Insufficient permissions (admin-only operations)
- **404 Not Found**: Resource doesn't exist

## Extension Points

1. **Add Email Notifications**: Extend survey submission handlers
2. **Add Analytics**: Implement aggregation queries in CRUD layer
3. **Add Pagination**: Modify list endpoints in routers
4. **Add Search**: Extend survey/poll queries in CRUD layer
5. **Add Rate Limiting**: Middleware in main.py
6. **Add Logging**: Decorator pattern on route handlers
