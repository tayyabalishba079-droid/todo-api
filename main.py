from fastapi import FastAPI

app = FastAPI()

# Root endpoint (Stage 1)
@app.get("/")
def get_info():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health endpoint (Stage 1)
@app.get("/health")
def get_health():
    return {"status": "ok"}