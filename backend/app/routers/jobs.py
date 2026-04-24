"""Jobs router."""
import logging
import json
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, JobStatus
from app.schemas.job import JobResponse, DiarizedTranscript, StandardTranscript, ErrorResponse
from app.s3_client import s3_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    """Get job status and metadata."""
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/jobs/{job_id}/result")
async def get_job_result(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    """Get transcription result."""
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        if job.status == JobStatus.QUEUED or job.status == JobStatus.PROCESSING:
            return {
                "status": job.status,
                "message": "Job is still processing",
            }

        if job.status == JobStatus.FAILED:
            return {
                "status": JobStatus.FAILED,
                "error": job.error_message,
            }

        # Fetch result from S3
        transcript_key = f"results/{job_id}/transcript.json"
        
        # Download from S3 and parse
        import io
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        if s3_client.download_file(transcript_key, tmp_path):
            with open(tmp_path, 'r') as f:
                transcript_data = json.load(f)
            
            import os
            os.remove(tmp_path)
            
            return {
                "status": JobStatus.COMPLETED,
                "job_id": str(job_id),
                "filename": job.filename,
                "diarization_enabled": job.diarization_enabled,
                "transcript": transcript_data,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve result",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/jobs/{job_id}/status")
async def get_simple_status(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    """Get job status only."""
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return {"job_id": str(job_id), "status": job.status}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
