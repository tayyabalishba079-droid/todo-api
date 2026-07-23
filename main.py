import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

DB_FILE = "tasks.db"

# Validation models
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        initial_tasks = [
            ("Buy groceries", False),
            ("Study FastAPI", True),
            ("Complete W3 Assignment", False)
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)", 
            initial_tasks
        )
        conn.commit()
    conn.close()

init_db()

# Root & Health
@app.get("/")
def get_info():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def get_health():
    return {"status": "ok"}

# Read Endpoints
@app.get("/tasks")
def get_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    tasks = []
    for row in rows:
        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })
    return tasks

@app.get("/tasks/{id}")
def get_single_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

# Create Endpoint
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if len(task_data.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task_data.title.strip(), False)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": new_id,
        "title": task_data.title.strip(),
        "done": False
    }

# Update Endpoint
@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_title = row["title"]
    current_done = bool(row["done"])
    
    new_title = current_title
    if task_data.title is not None:
        if len(task_data.title.strip()) == 0:
            conn.close()
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        new_title = task_data.title.strip()
        
    new_done = task_data.done if task_data.done is not None else current_done
    
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, id)
    )
    conn.commit()
    conn.close()
    
    return {
        "id": id,
        "title": new_title,
        "done": new_done
    }

# Delete Endpoint
@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return