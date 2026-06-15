"""Application constants."""

# HTTP Status Messages
SUCCESS_MESSAGES = {
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
}

ERROR_MESSAGES = {
    "NOT_FOUND": "Resource not found",
    "ALREADY_EXISTS": "Resource already exists",
    "UNAUTHORIZED": "Unauthorized access",
    "FORBIDDEN": "Access forbidden",
    "INVALID_CREDENTIALS": "Invalid credentials",
    "INVALID_TOKEN": "Invalid token",
}

# Database
DB_ECHO = False

# User Roles
ROLES = {
    "USER": "user",
    "ADMIN": "admin",
}

# Question Types
QUESTION_TYPES = {
    "MCQ": "mcq",
    "TEXT": "text",
}
