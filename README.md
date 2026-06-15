# Poll Application

A comprehensive FastAPI-based survey and polling platform with JWT authentication, role-based access control, and PostgreSQL database.

## Features

- **User Authentication**: JWT bearer token authentication with secure password hashing (bcrypt)
- **Role-Based Access Control**: Support for `user` and `admin` roles
- **Survey Management**: Create, read, update, and delete surveys with multiple question types (MCQ, text)
- **Poll Management**: Create and manage polls with multiple voting options
- **User Submissions**: Authenticated users can submit survey responses and vote on polls
- **Admin Dashboard**: View all survey submissions and poll votes
- **Automatic User Attribution**: Survey submissions and poll votes are automatically attributed to the authenticated user
- **API Documentation**: Interactive Swagger UI and ReDoc documentation

## Project Structure

```
poll/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main FastAPI application
│   ├── auth.py                 # JWT authentication and authorization
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy ORM models
│   ├── crud/                   # CRUD operations
│   │   ├── __init__.py
│   │   ├── users.py            # User operations
│   │   ├── surveys.py          # Survey operations
│   │   └── polls.py            # Poll operations
│   ├── schemas/                # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── users.py            # User schemas
│   │   ├── surveys.py          # Survey schemas
│   │   ├── polls.py            # Poll schemas
│   │   └── dashboard.py        # Dashboard schemas
│   └── routers/                # API route handlers
│       ├── __init__.py
│       ├── users.py            # Authentication routes
│       ├── surveys.py          # Survey routes
│       ├── polls.py            # Poll routes
│       └── admin.py            # Admin routes
├── env/                        # Python virtual environment
├── main.py                     # Application entry point
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

### Setup

1. **Clone/Navigate to the project directory**

```bash
cd d:\Practice\poll
```

2. **Create and activate virtual environment**

```bash
# Windows
python -m venv env
env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure PostgreSQL Database**

Create a PostgreSQL database:

```sql
CREATE DATABASE poll;
```

Update database URL in `app/database.py` if needed:

```python
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/poll'
```

5. **Run the application**

```bash
python main.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| POST | `/api/users` | Register a new user | No |
| POST | `/api/token` | Login and get JWT token | No |
| GET | `/api/me` | Get current user info | Yes |

### Surveys

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---|---|
| POST | `/api/surveys` | Create survey | Yes | admin |
| GET | `/api/surveys` | List all surveys | Yes | - |
| GET | `/api/surveys/{id}` | Get survey details | Yes | - |
| PUT | `/api/surveys/{id}` | Update survey | Yes | admin |
| DELETE | `/api/surveys/{id}` | Delete survey | Yes | admin |
| POST | `/api/surveys/submit` | Submit survey response | Yes | - |

### Polls

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---|---|
| POST | `/api/polls` | Create poll | Yes | admin |
| GET | `/api/polls` | List all polls | Yes | - |
| GET | `/api/polls/{id}` | Get poll details | Yes | - |
| PUT | `/api/polls/{id}` | Update poll | Yes | admin |
| DELETE | `/api/polls/{id}` | Delete poll | Yes | admin |
| POST | `/api/polls/{id}/vote` | Vote on poll | Yes | - |

### Admin

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---|---|
| GET | `/api/admin/dashboard` | View all submissions & votes | Yes | admin |

## Authentication Flow

### 1. Register User

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123",
    "role": "user"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "role": "user"
}
```

### 2. Login to Get Token

```bash
curl -X POST "http://localhost:8000/api/token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Token in Requests

```bash
curl -X GET "http://localhost:8000/api/surveys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Key Implementation Details

### User Authentication and Authorization

- **JWT Bearer Tokens**: Uses Python-Jose for JWT token creation and validation
- **Password Hashing**: Uses bcrypt via Passlib for secure password storage
- **Role-Based Access**: 
  - `admin`: Can create, update, delete surveys and polls
  - `user`: Can read surveys/polls and submit responses/votes

### Automatic User Attribution

**Important**: Survey submissions and poll votes are automatically attributed to the authenticated user:

- **Survey Submission**: The `submitted_by` field is automatically set to the authenticated user's username
- **Poll Vote**: The `voter_id` field is automatically set to the authenticated user's username
- **User Registration**: Only registered users in the database can submit surveys or vote on polls

### Database Models

1. **User**: Stores user credentials with hashed passwords and roles
2. **Survey**: Survey container with title and description
3. **Question**: Survey questions (MCQ or text type)
4. **Option**: Multiple choice options for questions
5. **SurveySubmission**: User survey submissions
6. **Answer**: User answers to survey questions
7. **Poll**: Poll container with title and description
8. **PollOption**: Poll voting options
9. **PollVote**: Individual votes on poll options

## Example Usage

### Create a Survey (Admin Only)

```bash
curl -X POST "http://localhost:8000/api/surveys" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Satisfaction Survey",
    "description": "Please rate your experience",
    "questions": [
      {
        "question_text": "How satisfied are you?",
        "question_type": "mcq",
        "options": [
          {"option_text": "Very Satisfied"},
          {"option_text": "Satisfied"},
          {"option_text": "Neutral"},
          {"option_text": "Dissatisfied"}
        ]
      }
    ]
  }'
```

### Submit Survey Response (Authenticated User)

```bash
curl -X POST "http://localhost:8000/api/surveys/submit" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "survey_id": 1,
    "answers": [
      {
        "question_id": 1,
        "selected_option_id": 1
      }
    ]
  }'
```

### Create a Poll (Admin Only)

```bash
curl -X POST "http://localhost:8000/api/polls" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "What is your favorite programming language?",
    "description": "Cast your vote",
    "options": [
      {"option_text": "Python"},
      {"option_text": "JavaScript"},
      {"option_text": "Go"},
      {"option_text": "Rust"}
    ]
  }'
```

### Vote on Poll (Authenticated User)

```bash
curl -X POST "http://localhost:8000/api/polls/1/vote" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "option_id": 1
  }'
```

### View Admin Dashboard (Admin Only)

```bash
curl -X GET "http://localhost:8000/api/admin/dashboard" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## Security Considerations

1. **SECRET_KEY**: In production, store `SECRET_KEY` in environment variables, not in code
2. **DATABASE_URL**: Store database credentials in environment variables
3. **HTTPS**: Always use HTTPS in production
4. **CORS**: Configure CORS appropriately for your frontend domain
5. **Rate Limiting**: Consider implementing rate limiting for production
6. **Input Validation**: All inputs are validated using Pydantic schemas

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Dependencies

See `requirements.txt` for the complete list. Key dependencies:

- FastAPI: Modern web framework
- SQLAlchemy: ORM for database operations
- Pydantic: Data validation
- python-jose: JWT token handling
- passlib[bcrypt]: Password hashing
- psycopg2: PostgreSQL adapter
- uvicorn: ASGI server

## Running Tests

To verify the setup, you can run a quick import test:

```bash
python -c "from app import main; print('✓ Application initialized successfully')"
```

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and the database URL is correct:

```bash
# Test PostgreSQL connection
psql -U postgres -d poll
```

### Import Errors

Ensure you're in the correct directory and virtual environment is activated:

```bash
# Verify virtual environment
which python  # on Linux/Mac
where python  # on Windows
```

### Token Validation Errors

- Ensure the token hasn't expired (default: 60 minutes)
- Verify the token format: `Authorization: Bearer <token>`
- Check that the user still exists in the database

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to the FastAPI documentation:
- https://fastapi.tiangolo.com/
- https://docs.sqlalchemy.org/
