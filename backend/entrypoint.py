"""Entrypoint for backend."""
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Initialize database on startup
    from app.database import init_db
    from app.s3_client import s3_client
    
    logger.info("Initializing database...")
    init_db()
    logger.info("Creating S3 bucket...")
    s3_client.create_bucket()
    logger.info("Startup complete")
