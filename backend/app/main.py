

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from uuid import uuid4

app = FastAPI(
    title="EcoSched API",
    description="Carbon-Aware Cloud Job Scheduling Platform",
    version="1.0.0"
)

# Temporary storage for submitted jobs
jobs = []


# Job request structure
class JobCreate(BaseModel):

    job_name: str = Field(min_length=3, max_length=100)

    estimated_runtime_minutes: int = Field(gt=0)

    deadline: datetime

    preferred_region: str

    scheduling_mode: Literal[
        "greenest",
        "fastest",
        "balanced"
    ]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to EcoSched!",
        "status": "Backend is running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Submit a new job
@app.post("/jobs")
def submit_job(job: JobCreate):

    new_job = {
        "id": str(uuid4()),
        "job_name": job.job_name,
        "estimated_runtime_minutes": job.estimated_runtime_minutes,
        "deadline": job.deadline.isoformat(),
        "preferred_region": job.preferred_region,
        "scheduling_mode": job.scheduling_mode,
        "status": "pending"
    }

    jobs.append(new_job)

    return {
        "message": "Job submitted successfully!",
        "job": new_job
    }


# Retrieve all submitted jobs
@app.get("/jobs")
def get_jobs():
    return {
        "total_jobs": len(jobs),
        "jobs": jobs
    }
