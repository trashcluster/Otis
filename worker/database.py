"""Worker database operations."""
import logging
from datetime import datetime
from uuid import UUID
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import sessionmaker, declarative_base
import enum

from config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class JobStatus(str, enum.Enum):
    """Job status."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    """Job model."""
    __tablename__ = "jobs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(512), nullable=False, unique=True)
    diarization_enabled = Column(Boolean, default=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.QUEUED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)


def get_job(job_id: UUID) -> Job:
    """Get job by ID."""
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        return job
    finally:
        db.close()


def update_job_status(job_id: UUID, status: JobStatus, error_message: str = None):
    """Update job status."""
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = status
            if status == JobStatus.COMPLETED:
                job.completed_at = datetime.utcnow()
            if error_message:
                job.error_message = error_message
            db.commit()
            logger.info(f"Job {job_id} status updated to {status}")
    except Exception as e:
        logger.error(f"Error updating job status: {e}")
        db.rollback()
    finally:
        db.close()
