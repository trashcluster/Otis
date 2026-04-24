"""Main worker process."""
import logging
import os
import tempfile
from uuid import UUID
from redis import Redis
from rq import Worker, Queue

from config import settings
from database import get_job, update_job_status, JobStatus
from s3_client import s3_client
from transcription import process_audio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_transcription(job_id: str, diarization_enabled: bool):
    """
    Process transcription job.
    
    Args:
        job_id: UUID of the job
        diarization_enabled: Whether to enable speaker diarization
    """
    logger.info(f"Processing job: {job_id}, diarization: {diarization_enabled}")
    
    try:
        # Convert to UUID
        job_uuid = UUID(job_id)
        
        # Update job status
        update_job_status(job_uuid, JobStatus.PROCESSING)
        
        # Get job from database
        job = get_job(job_uuid)
        if not job:
            logger.error(f"Job not found: {job_id}")
            return
        
        # Download file from S3
        logger.info(f"Downloading file from S3: {job.s3_key}")
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        if not s3_client.download_file(job.s3_key, tmp_path):
            logger.error(f"Failed to download file from S3")
            update_job_status(job_uuid, JobStatus.FAILED, "Failed to download file from S3")
            return
        
        try:
            # Process audio
            logger.info(f"Processing audio file: {tmp_path}")
            result = process_audio(tmp_path, diarization_enabled)
            
            # Upload result to S3
            result_key = f"results/{job_id}/transcript.json"
            logger.info(f"Uploading result to S3: {result_key}")
            if not s3_client.upload_json(result, result_key):
                logger.error(f"Failed to upload result to S3")
                update_job_status(job_uuid, JobStatus.FAILED, "Failed to upload result to S3")
                return
            
            # Update job status
            update_job_status(job_uuid, JobStatus.COMPLETED)
            logger.info(f"Job completed: {job_id}")
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.info(f"Cleaned up temp file: {tmp_path}")
    
    except Exception as e:
        logger.error(f"Job processing failed: {e}", exc_info=True)
        try:
            job_uuid = UUID(job_id)
            update_job_status(job_uuid, JobStatus.FAILED, str(e))
        except Exception as e2:
            logger.error(f"Failed to update job status: {e2}")


def start_worker():
    """Start RQ worker."""
    redis_conn = Redis.from_url(settings.REDIS_URL)
    queue = Queue(connection=redis_conn)
    
    logger.info("Starting worker...")
    worker = Worker([queue], connection=redis_conn)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    start_worker()
