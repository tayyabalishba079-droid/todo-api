from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# In-memory database (3 initial tasks)
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Complete W2 Assignment", "done": False}
]

# Validation models
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

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

# Stage 3 Endpoint: Create
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    if len(task_data.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    return new_task

# Stage 4 Endpoints: Update & Delete
@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    for task in tasks:
        if task["id"] == id:
            if task_data.title is not None:
                if len(task_data.title.strip()) == 0:
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_data.title.strip()
            if task_data.done is not None:
                task["done"] = task_data.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Task {id} not found")