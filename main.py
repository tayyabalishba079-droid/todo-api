from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory database (3 initial tasks)
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Complete W2 Assignment", "done": False}
]

# Stage 1 Endpoints
@app.get("/")
def get_info():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def get_health():
    return {"status": "ok"}

# Stage 2 Endpoints: Get all tasks & Get single task
@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_single_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    # Agar task na mile toh 404 error
    raise HTTPException(status_code=404, detail=f"Task {id} not found")