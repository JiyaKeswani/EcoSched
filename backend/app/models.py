
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)

    job_name = Column(String(100), nullable=False)

    estimated_runtime_minutes = Column(Integer, nullable=False)

    deadline = Column(DateTime(timezone=True), nullable=False)

    preferred_region = Column(String(50), nullable=False)

    scheduling_mode = Column(String(20), nullable=False)

    status = Column(String(20), default="pending")
