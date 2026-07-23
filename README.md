# Todo API (FastAPI)

A lightweight FastAPI application providing full CRUD operations for task management.

## Features & Endpoints

- `GET /` - API Root Info (Stage 1)
- `GET /health` - Health Check Endpoint (Stage 1)
- `GET /tasks` - Retrieve all tasks (Stage 2)
- `GET /tasks/{id}` - Retrieve a single task with 404 handling (Stage 2)
- `POST /tasks` - Create a new task with Pydantic validation (Stage 3)
- `PUT /tasks/{id}` - Update a task (Stage 4)
- `DELETE /tasks/{id}` - Delete a task with 204 No Content status (Stage 4)

## Interactive API Docs

Once running locally, access the interactive Swagger documentation at:
`http://127.0.0.1:8000/docs`