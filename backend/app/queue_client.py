"""Queue client for job management."""
import logging
from redis import Redis
from rq import Queue
from rq.job import Job as RQJob
from app.config import settings

logger = logging.getLogger(__name__)


class QueueClient:
    """Wrapper for Redis queue operations."""

    def __init__(self):
        """Initialize queue client."""
        # Parse Redis URL
        redis_url = settings.REDIS_URL
        self.redis_conn = Redis.from_url(redis_url, decode_responses=True)
        self.queue = Queue(connection=self.redis_conn)

    def enqueue_job(self, job_id: str, diarization_enabled: bool) -> bool:
        """Enqueue transcription job."""
        try:
            # Enqueue job using function path reference
            # Worker will import and execute the function
            self.queue.enqueue(
                'worker.process_transcription',
                job_id=str(job_id),
                diarization_enabled=diarization_enabled,
            )
            logger.info(f"Job enqueued: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error enqueuing job: {e}")
            return False

    def get_job_status(self, job_id: str) -> str:
        """Get job status from queue."""
        try:
            job = self.queue.fetch_job(job_id)
            if job:
                return job.get_status()
            return None
        except Exception as e:
            logger.error(f"Error getting job status: {e}")
            return None


# Singleton instance
queue_client = QueueClient()
