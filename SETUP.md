# Setup and Deployment Guide

## Prerequisites

- Docker & Docker Compose (for containerized deployment)
- Python 3.11+ (for local development)
- Node.js 20+ (for frontend development)
- OpenAI API key (required for transcription)

## Quick Start with Docker Compose

### 1. Clone Repository
```bash
git clone https://github.com/trashcluster/otis.git
cd otis
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Start All Services
```bash
docker-compose up -d
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (user: minioadmin, pass: minioadmin)

### 5. Verify Services
```bash
# Check all containers are running
docker-compose ps

# View logs
docker-compose logs -f
```

---

## Local Development Setup

### Backend

#### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Database & Services
Ensure PostgreSQL, Redis, and MinIO are running (via Docker Compose):
```bash
docker-compose up postgres redis minio -d
```

#### 4. Run Backend
```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

---

### Worker

#### 1. Create Virtual Environment
```bash
cd ../worker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run Worker
```bash
python worker.py
```

The worker will start consuming jobs from Redis queue.

---

### Frontend

#### 1. Install Dependencies
```bash
cd ../frontend
npm install
```

#### 2. Run Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

#### 3. Build for Production
```bash
npm run build
```

---

## Docker Build & Push

### Build Images Locally

```bash
# Backend
docker build -t trashcluster/otis-backend:v1.0.0 ./backend

# Worker
docker build -t trashcluster/otis-worker:v1.0.0 ./worker

# Frontend
docker build -t trashcluster/otis-frontend:v1.0.0 ./frontend
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Backend
docker push trashcluster/otis-backend:v1.0.0
docker tag trashcluster/otis-backend:v1.0.0 trashcluster/otis-backend:latest
docker push trashcluster/otis-backend:latest

# Worker
docker push trashcluster/otis-worker:v1.0.0
docker tag trashcluster/otis-worker:v1.0.0 trashcluster/otis-worker:latest
docker push trashcluster/otis-worker:latest

# Frontend
docker push trashcluster/otis-frontend:v1.0.0
docker tag trashcluster/otis-frontend:v1.0.0 trashcluster/otis-frontend:latest
docker push trashcluster/otis-frontend:latest
```

---

## Using Custom Image Tags

To use a specific image version/tag:

```bash
# Using v1.0.0
IMAGE_TAG=v1.0.0 docker-compose up -d

# Using latest (default)
docker-compose up -d
```

---

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs worker
docker-compose logs frontend

# Restart services
docker-compose restart
```

### Database connection errors
```bash
# Wait for postgres to be ready
docker-compose up postgres
# Wait 10 seconds for startup
sleep 10
docker-compose up -d
```

### MinIO bucket not accessible
```bash
# Manual bucket creation
docker exec otis-minio mc mb minio/otis
```

### Memory issues
Increase Docker resource limits:
```bash
# In docker-compose.yml, add to services:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
```

---

## Production Deployment

### Recommendations

1. **Use managed services**:
   - AWS RDS for PostgreSQL
   - AWS ElastiCache for Redis
   - AWS S3 for storage
   - AWS Secrets Manager for API keys

2. **Load balancing**:
   - Use multiple worker instances
   - nginx or AWS ELB for frontend/backend

3. **Security**:
   - Implement API authentication
   - Use HTTPS/TLS
   - Enable CORS restrictions
   - Use environment-based secrets management

4. **Monitoring**:
   - ELK stack or AWS CloudWatch for logging
   - Prometheus for metrics
   - PagerDuty/Slack for alerts

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                  │
│              http://localhost:3000                  │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│               Backend API (FastAPI)                 │
│              http://localhost:8000                  │
│  ┌────────────────────────────────────────────┐    │
│  │  Upload, Job Status, Results Endpoints     │    │
│  └────────────────────────────────────────────┘    │
└────┬─────────────────┬──────────────────────┬───────┘
     │                 │                      │
     ▼                 ▼                      ▼
┌─────────┐      ┌─────────┐          ┌────────────┐
│PostgreSQL│      │  Redis  │          │   MinIO    │
│ Database │      │  Queue  │          │   S3       │
└─────────┘      └─────────┘          └────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │  Worker Service  │
            │ (OpenAI Transcribe)│
            └──────────────────┘
```

---

## Database Schema

See `init.sql` for initial schema creation.

**jobs table**:
- `id` (UUID): Primary key
- `filename` (varchar): Original filename
- `s3_key` (varchar): Path in S3/MinIO
- `diarization_enabled` (boolean): Whether diarization was requested
- `status` (varchar): queued | processing | completed | failed
- `created_at` (timestamp): Creation time
- `completed_at` (timestamp): Completion time (if done)
- `error_message` (text): Error details (if failed)

---

## Support

For issues, see [API.md](API.md) for endpoint documentation and example requests.
