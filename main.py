# Project: FastAPI User & Model Service
"""
A robust FastAPI application for user management and model-based responses.
Features:
- User CRUD endpoints
- Model response endpoint
- Logging
- CORS support
- Pydantic models
"""

from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import logging
from model import get_response

app = FastAPI(title="User API", description="A robust FastAPI example.", version="2.0")

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Allow all origins for development (customize for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class ModelPrompt(BaseModel):
    prompt: str

class ModelResponse(BaseModel):
    response: str

# In-memory database
users: List[Dict[str, Any]] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

def get_next_id() -> int:
    """Get the next user ID."""
    return max((u["id"] for u in users), default=0) + 1

def find_user(user_id: int) -> Dict[str, Any]:
    """Find a user by ID."""
    return next((u for u in users if u["id"] == user_id), None)

@app.get("/", tags=["Root"])
def home() -> Dict[str, Any]:
    """Returns a welcome message."""
    return {"message": "Welcome to the robust FastAPI!"}

@app.get("/users", response_model=List[User], tags=["Users"])
def get_users() -> List[User]:
    """Returns a list of all users."""
    return users

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int) -> User:
    """Returns a single user by their ID."""
    user = find_user(user_id)
    if user:
        return user
    logging.warning(f"User with ID {user_id} not found.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def add_user(new_user: UserCreate) -> User:
    """Adds a new user to the list."""
    if any(u["email"] == new_user.email for u in users):
        logging.warning(f"Attempt to add duplicate email: {new_user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user_data = {
        "id": get_next_id(),
        "name": new_user.name,
        "email": new_user.email
    }
    users.append(new_user_data)
    logging.info(f"Added user: {new_user_data}")
    return new_user_data

@app.post("/model-response", response_model=ModelResponse, tags=["Model"])
def model_response(data: ModelPrompt) -> ModelResponse:
    """Returns the model's response for a given prompt."""
    if not data.prompt or not data.prompt.strip():
        logging.warning("Empty prompt received for model-response.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt cannot be empty")
    result = get_response(data.prompt)
    return ModelResponse(response=result)
