"""FastAPI application factory and main entry point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.s3_client import s3_client
from app.routers import upload, jobs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting up application...")
    init_db()
    s3_client.create_bucket()
    logger.info("Application startup complete")
    yield
    # Shutdown
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Otis API",
        description="Audio Transcription API with Speaker Diarization",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(upload.router, tags=["Upload"])
    app.include_router(jobs.router, tags=["Jobs"])

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Otis Audio Transcription API",
            "version": "1.0.0",
            "docs": "/docs",
        }

    return app


# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
