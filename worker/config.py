"""Worker configuration."""
import os
from pydantic_settings import BaseSettings


class WorkerSettings(BaseSettings):
    """Worker settings."""

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/otis"

    # S3 / Minio
    S3_ENDPOINT: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "otis"
    S3_REGION: str = "us-east-1"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Worker
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = WorkerSettings()
