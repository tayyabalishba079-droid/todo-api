from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# In-memory database (3 initial tasks)
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Complete W2 Assignment", "done": False}
]

# Validation model for POST body
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

# Stage 1 Endpoints
@app.get("/")
def get_info():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def get_health():
    return {"status": "ok"}

# Stage 2 Endpoints: Read operations
@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_single_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

# Stage 3 Endpoint: Create a new task
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    # Validation: empty string check
    if len(task_data.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    # Auto-generate next ID
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    return new_task