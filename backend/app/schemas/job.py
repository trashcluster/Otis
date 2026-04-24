"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models import JobStatus


class JobBase(BaseModel):
    """Base job schema."""
    filename: str
    diarization_enabled: bool = False


class JobCreate(JobBase):
    """Job creation request."""
    pass


class JobResponse(JobBase):
    """Job response."""
    id: UUID
    s3_key: str
    status: JobStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    """Upload endpoint response."""
    job_id: UUID
    filename: str
    diarization_enabled: bool
    message: str = "File uploaded successfully"


class TranscriptSegment(BaseModel):
    """Transcript segment (for diarization)."""
    speaker: str
    start: float
    end: float
    text: str


class DiarizedTranscript(BaseModel):
    """Diarized transcript format."""
    segments: List[TranscriptSegment]


class StandardTranscript(BaseModel):
    """Standard transcript format."""
    text: str


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    error_code: Optional[str] = None
