"""File upload router."""
import logging
import io
import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, JobStatus
from app.schemas.job import UploadResponse, ErrorResponse
from app.s3_client import s3_client
from app.queue_client import queue_client
from app.config import settings
from app.utils import is_allowed_extension, get_file_extension

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    diarization: bool = Form(False),
    db: Session = Depends(get_db),
):
    """
    Upload audio file for transcription.
    
    - **file**: Audio file (wav, mp3, m4a, flac, ogg)
    - **diarization**: Enable speaker diarization
    """
    try:
        # Validate file extension
        filename = file.filename
        if not is_allowed_extension(filename, settings.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            )

        # Read file content
        content = await file.read()
        
        # Check file size
        file_size = len(content)
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds limit of {settings.MAX_FILE_SIZE / (1024*1024):.0f}MB",
            )

        # Create job in database
        job = Job(
            filename=filename,
            s3_key=f"uploads/{os.urandom(16).hex()}/{filename}",
            diarization_enabled=diarization,
            status=JobStatus.QUEUED,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        logger.info(f"Job created: {job.id}")

        # Upload to S3
        file_obj = io.BytesIO(content)
        if not s3_client.upload_fileobj(file_obj, job.s3_key):
            job.status = JobStatus.FAILED
            job.error_message = "Failed to upload file to S3"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload file",
            )

        logger.info(f"File uploaded to S3: {job.s3_key}")

        # Enqueue job
        if not queue_client.enqueue_job(str(job.id), diarization):
            job.status = JobStatus.FAILED
            job.error_message = "Failed to enqueue job"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to enqueue job",
            )

        logger.info(f"Job enqueued: {job.id}")

        return UploadResponse(
            job_id=job.id,
            filename=filename,
            diarization_enabled=diarization,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
