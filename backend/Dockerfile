# Multi-stage backend builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Final backend stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 otis

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/otis/.local
ENV PATH=/home/otis/.local/bin:$PATH

# Copy application code
COPY --chown=otis:otis app ./app
COPY --chown=otis:otis entrypoint.py .

# Switch to non-root user
USER otis

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default environment
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql://postgres:postgres@postgres:5432/otis
ENV REDIS_URL=redis://redis:6379/0
ENV S3_ENDPOINT=http://minio:9000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
