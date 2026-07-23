import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tododb")

app = FastAPI()

# Validation Models
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

# PostgreSQL Connection Helper (with retry logic for docker startup)
def get_db_connection():
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except psycopg2.OperationalError:
            if i == max_retries - 1:
                raise
            time.sleep(2)

# Database Setup (PostgreSQL)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()["count"]
    
    if count == 0:
        initial_tasks = [
            ("Buy groceries", False),
            ("Study FastAPI & PostgreSQL", True),
            ("Complete BE-04 Assignment", False)
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            initial_tasks
        )
        conn.commit()
        
    cursor.close()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

# Root & Health Endpoints
@app.get("/")
def get_info():
    return {"name": "Task API (PostgreSQL Stack)", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def get_health():
    return {"status": "ok"}

# Read Endpoints
@app.get("/tasks")
def get_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks ORDER BY id ASC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

@app.get("/tasks/{id}")
def get_single_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

# Create Endpoint
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if len(task_data.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done",
        (task_data.title.strip(), False)
    )
    new_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    return new_task

# Update Endpoint
@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()
    
    if task is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_title = task["title"]
    current_done = task["done"]
    
    new_title = current_title
    if task_data.title is not None:
        if len(task_data.title.strip()) == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        new_title = task_data.title.strip()
        
    new_done = task_data.done if task_data.done is not None else current_done
    
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
        (new_title, new_done, id)
    )
    updated_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    return updated_task

# Delete Endpoint
@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()
    
    if task is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return