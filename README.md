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



# Todo API (FastAPI with SQLite Database)

A lightweight FastAPI application providing full CRUD operations for task management integrated with SQLite database persistence.

## Features & Persistence

- **Database:** Stored in a local `tasks.db` SQLite file.
- **Auto Creation:** Automatically creates the `tasks` table and initial seed data if the database does not exist.
- **Persistence:** Data survives server restarts.

## Endpoints

- `GET /` - API Root Info
- `GET /health` - Health Check Endpoint
- `GET /tasks` - Retrieve all tasks from SQL database
- `GET /tasks/{id}` - Retrieve a single task with 404 error handling
- `POST /tasks` - Insert a new task into SQLite database
- `PUT /tasks/{id}` - Update an existing task row
- `DELETE /tasks/{id}` - Remove a task from SQLite database

## Example SQL Queries Used

```sql
-- Retrieve all tasks
SELECT id, title, done FROM tasks;

-- Insert a new task
INSERT INTO tasks (title, done) VALUES ('Buy milk', 0);

-- Update task
UPDATE tasks SET done = 1 WHERE id = 1;