
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Job

app = FastAPI(
    title="EcoSched API",
    description="Carbon-Aware Cloud Job Scheduling Platform",
    version="1.0.0"
)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Submit a job to PostgreSQL
@app.post("/jobs")
def submit_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):

    new_job = Job(
        id=str(uuid4()),
        job_name=job.job_name,
        estimated_runtime_minutes=job.estimated_runtime_minutes,
        deadline=job.deadline,
        preferred_region=job.preferred_region,
        scheduling_mode=job.scheduling_mode,
        status="pending"
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job submitted successfully!",
        "job": {
            "id": new_job.id,
            "job_name": new_job.job_name,
            "estimated_runtime_minutes": new_job.estimated_runtime_minutes,
            "deadline": new_job.deadline,
            "preferred_region": new_job.preferred_region,
            "scheduling_mode": new_job.scheduling_mode,
            "status": new_job.status
        }
    }


# Retrieve jobs from PostgreSQL
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    all_jobs = db.query(Job).all()

    return {
        "total_jobs": len(all_jobs),
        "jobs": all_jobs
    }
