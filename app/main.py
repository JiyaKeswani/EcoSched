
from fastapi import FastAPI

app = FastAPI(
    title="EcoSched API",
    description="Carbon-Aware Cloud Job Scheduling Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to EcoSched!",
        "status": "Backend is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
