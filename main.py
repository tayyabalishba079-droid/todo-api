import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Database File Name
DB_FILE = "tasks.db"

# Helper Function: Database Connection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Returns dict-like rows
    return conn

# Database Initialization Function
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tasks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    # Insert 3 example tasks if table is empty
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

# Run database setup on startup
init_db()

# Stage 1 Root & Health Endpoints
@app.get("/")
def get_info():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def get_health():
    return {"status": "ok"}