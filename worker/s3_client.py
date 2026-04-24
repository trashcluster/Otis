"""Worker S3 client."""
import logging
from botocore.exceptions import ClientError
import boto3
from config import settings

logger = logging.getLogger(__name__)


class S3Client:
    """S3 operations wrapper."""

    def __init__(self):
        """Initialize S3 client."""
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket = settings.S3_BUCKET

    def download_file(self, s3_key: str, local_path: str) -> bool:
        """Download file from S3."""
        try:
            self.client.download_file(self.bucket, s3_key, local_path)
            logger.info(f"Downloaded from S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return False

    def upload_json(self, data: dict, s3_key: str) -> bool:
        """Upload JSON to S3."""
        import json
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=json.dumps(data),
                ContentType="application/json",
            )
            logger.info(f"Uploaded JSON to S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading JSON: {e}")
            return False


s3_client = S3Client()
