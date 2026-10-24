#### just a demo made during SIH  
# FastAPI User & Model Service

A robust FastAPI application for user management and model-based responses.

## Features
- User CRUD endpoints
- Model response endpoint
- Logging
- CORS support
- Pydantic models

## Setup Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

3. **API Endpoints**
   - `GET /users` — List all users
   - `GET /users/{user_id}` — Get user by ID
   - `POST /users` — Add a new user
   - `POST /model-response` — Get model response for a prompt

## Notes
- The model endpoint uses `ollama` and expects the model `career` to be available.
- For production, update CORS settings and consider using a real database.
- well this is my first api project so please be gentle <3 
