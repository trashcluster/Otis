"""S3 client for object storage operations."""
import logging
import boto3
from botocore.exceptions import ClientError
from app.config import settings

logger = logging.getLogger(__name__)


class S3Client:
    """Wrapper for S3 operations."""

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

    def create_bucket(self) -> bool:
        """Create bucket if it doesn't exist."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
            logger.info(f"Bucket {self.bucket} already exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                try:
                    self.client.create_bucket(Bucket=self.bucket)
                    logger.info(f"Bucket {self.bucket} created")
                    return True
                except ClientError as e:
                    logger.error(f"Error creating bucket: {e}")
                    return False
            else:
                logger.error(f"Error checking bucket: {e}")
                return False

    def upload_file(self, file_path: str, s3_key: str) -> bool:
        """Upload file to S3."""
        try:
            self.client.upload_file(file_path, self.bucket, s3_key)
            logger.info(f"File uploaded to S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False

    def upload_fileobj(self, file_obj, s3_key: str) -> bool:
        """Upload file object to S3."""
        try:
            self.client.upload_fileobj(file_obj, self.bucket, s3_key)
            logger.info(f"File object uploaded to S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file object: {e}")
            return False

    def download_file(self, s3_key: str, file_path: str) -> bool:
        """Download file from S3."""
        try:
            self.client.download_file(self.bucket, s3_key, file_path)
            logger.info(f"File downloaded from S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return False

    def upload_json(self, data: dict, s3_key: str) -> bool:
        """Upload JSON data to S3."""
        import json
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=json.dumps(data),
                ContentType="application/json",
            )
            logger.info(f"JSON uploaded to S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading JSON: {e}")
            return False


# Singleton instance
s3_client = S3Client()
