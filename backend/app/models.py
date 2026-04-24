"""SQLAlchemy models for database schema."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.database import Base


class JobStatus(str, enum.Enum):
    """Job status enum."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    """Job model for tracking transcription requests."""
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(512), nullable=False, unique=True)
    diarization_enabled = Column(Boolean, default=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.QUEUED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Job(id={self.id}, filename={self.filename}, status={self.status})>"
