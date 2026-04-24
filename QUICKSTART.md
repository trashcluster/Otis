# 🚀 Quick Reference Guide

## Getting Started in 5 Minutes

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key (get at https://platform.openai.com/api-keys)

### Step 1: Clone & Configure
```bash
git clone https://github.com/trashcluster/otis.git
cd otis
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 2: Start Services
```bash
docker-compose up -d
```

### Step 3: Verify
```bash
docker-compose ps          # Check containers
docker-compose logs -f     # View logs
curl http://localhost:8000/health  # Test API
```

### Step 4: Access
- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin/admin)

---

## Common Commands

### Start/Stop Services
```bash
docker-compose up -d       # Start background
docker-compose down        # Stop all
docker-compose restart     # Restart
docker-compose logs -f     # View logs
```

### Check Status
```bash
docker-compose ps
docker-compose exec backend python -c "from app.database import SessionLocal; SessionLocal()"
```

### Scale Workers
```bash
docker-compose up -d --scale worker=3
```

### View Service Logs
```bash
docker-compose logs backend
docker-compose logs worker
docker-compose logs frontend
```

---

## Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Worker Development
```bash
cd worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python worker.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

---

## API Quick Examples

### 1. Upload Audio
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.mp3" \
  -F "diarization=true"

# Save job_id from response
```

### 2. Check Status
```bash
curl http://localhost:8000/jobs/$JOB_ID/status
```

### 3. Get Result
```bash
curl http://localhost:8000/jobs/$JOB_ID/result | jq
```

### 4. Full Example Script
```bash
#!/bin/bash
# Upload
JOB=$(curl -s -X POST http://localhost:8000/upload \
  -F "file=@audio.mp3" \
  -F "diarization=true")
JOB_ID=$(echo $JOB | jq -r '.job_id')
echo "Job ID: $JOB_ID"

# Poll status
while true; do
  STATUS=$(curl -s http://localhost:8000/jobs/$JOB_ID/status | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  sleep 2
done

# Get result
curl http://localhost:8000/jobs/$JOB_ID/result | jq '.transcript'
```

---

## File Structure Quick Reference

```
otis/
├── backend/          → FastAPI application
├── worker/           → RQ job processor
├── frontend/         → React web UI
├── docker-compose.yml → Service orchestration
├── init.sql          → Database schema
├── .env.example      → Configuration template
├── README.md         → Main documentation
├── SETUP.md          → Detailed setup guide
├── API.md            → API reference
└── IMPLEMENTATION.md → What was built
```

---

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs worker

# Rebuild
docker-compose down -v
docker-compose up -d
```

### Database errors
```bash
# Wait for postgres
docker-compose up postgres -d
sleep 10
docker-compose up -d
```

### API not responding
```bash
# Check backend health
curl http://localhost:8000/health

# Check containers
docker-compose ps

# View backend logs
docker-compose logs backend
```

### Frontend not loading
```bash
# Check frontend service
docker-compose logs frontend

# Verify backend connection
curl http://backend:8000/health  # from inside container
```

---

## Configuration

### Environment Variables
See `.env.example` for all options:
- `OPENAI_API_KEY` - Required for transcription
- `IMAGE_TAG` - Docker image version (default: latest)
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `S3_ENDPOINT` - S3/MinIO endpoint

### Docker Compose Override
Create `docker-compose.override.yml`:
```yaml
services:
  backend:
    environment:
      DEBUG: "true"
    ports:
      - "8001:8000"
```

---

## Performance Tips

### Database Optimization
- Indexes already created on `status` and `created_at`
- Consider `VACUUM ANALYZE` for production

### Worker Scaling
```bash
# Run multiple workers
docker-compose up -d --scale worker=5
```

### Memory Management
- Set max file size in `.env` if needed
- Monitor MinIO disk space

---

## Monitoring

### RQ Dashboard (optional)
```bash
# Install
pip install rq-dashboard

# Run
rq-dashboard -H redis -p 9181

# Access
http://localhost:9181
```

### PostgreSQL
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d otis

# View jobs table
SELECT * FROM jobs;
SELECT COUNT(*) FROM jobs WHERE status = 'completed';
```

### MinIO
```bash
# Console: http://localhost:9001
# Credentials: minioadmin/minioadmin

# List buckets
docker-compose exec minio mc ls minio

# List files
docker-compose exec minio mc ls minio/otis
```

---

## Docker Hub Push

```bash
# Build
docker build -t trashcluster/otis-backend:v1.0 ./backend
docker build -t trashcluster/otis-worker:v1.0 ./worker
docker build -t trashcluster/otis-frontend:v1.0 ./frontend

# Tag latest
docker tag trashcluster/otis-backend:v1.0 trashcluster/otis-backend:latest
docker tag trashcluster/otis-worker:v1.0 trashcluster/otis-worker:latest
docker tag trashcluster/otis-frontend:v1.0 trashcluster/otis-frontend:latest

# Push
docker login
docker push trashcluster/otis-backend:v1.0
docker push trashcluster/otis-backend:latest
docker push trashcluster/otis-worker:v1.0
docker push trashcluster/otis-worker:latest
docker push trashcluster/otis-frontend:v1.0
docker push trashcluster/otis-frontend:latest

# Use specific version
IMAGE_TAG=v1.0 docker-compose up -d
```

---

## Next Steps

1. ✅ Start with `docker-compose up -d`
2. ✅ Open http://localhost:3000
3. ✅ Upload a test audio file
4. ✅ Check API docs at http://localhost:8000/docs
5. ✅ Monitor worker logs: `docker-compose logs -f worker`
6. ✅ Review [SETUP.md](SETUP.md) for deeper customization

---

## Documentation Links

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Detailed setup & troubleshooting
- [API.md](API.md) - Complete API reference
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - What was built
- [PROMPT.md](PROMPT.md) - Original requirements

---

**Need help? Check the docs or run: `docker-compose logs -f`**
