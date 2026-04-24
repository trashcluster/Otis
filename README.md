# Otis - Audio Transcription Application

Otis is a production-ready web application for uploading audio files, processing them asynchronously, and returning transcriptions with optional speaker diarization powered by OpenAI.

## 🎯 Features

✅ **Drag-and-drop audio upload**
✅ **Asynchronous job processing** via Redis queue
✅ **Speaker diarization** support (optional)
✅ **S3-compatible storage** (MinIO/AWS S3)
✅ **RESTful API** with FastAPI
✅ **Modern React UI** with TypeScript & TailwindCSS
✅ **Docker-ready** with multi-stage builds
✅ **Production-grade** with error handling & retry logic

## 🏗️ Architecture

- **Frontend**: React 18 + TypeScript + TailwindCSS
- **Backend**: FastAPI (Python)
- **Worker**: RQ + OpenAI APIs for transcription
- **Database**: PostgreSQL
- **Queue**: Redis
- **Storage**: S3-compatible (MinIO or AWS S3)
- **Transcription**: OpenAI audio models

## 🚀 Quick Start

### Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/trashcluster/otis.git
cd otis

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# Start all services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Local Development

See [SETUP.md](SETUP.md) for detailed local setup instructions.

## 📁 Project Structure

```
otis/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── database.py          # DB session management
│   │   ├── config.py            # Configuration
│   │   ├── s3_client.py         # S3 operations
│   │   ├── queue_client.py      # Redis queue
│   │   ├── utils.py             # Utility functions
│   │   ├── routers/
│   │   │   ├── upload.py        # Upload endpoint
│   │   │   └── jobs.py          # Job endpoints
│   │   └── schemas/
│   │       └── job.py           # Pydantic models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── worker/
│   ├── worker.py                # RQ worker main
│   ├── config.py                # Worker config
│   ├── database.py              # DB operations
│   ├── s3_client.py             # S3 client
│   ├── transcription.py         # OpenAI integration
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUploader.tsx
│   │   │   ├── JobStatus.tsx
│   │   │   └── TranscriptViewer.tsx
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   ├── App.tsx              # Main app
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Styles
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml           # All services configuration
├── init.sql                     # Database schema
├── .env.example                 # Environment template
├── PROMPT.md                    # Original requirements
├── SETUP.md                     # Setup guide
├── API.md                       # API documentation
└── README.md                    # This file
```

## 🔧 Installation & Usage

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+ (local dev)
- Node.js 20+ (local dev)
- OpenAI API key

### Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
OPENAI_API_KEY=sk-your-key-here
IMAGE_TAG=latest
```

### Running Services

**Via Docker Compose:**
```bash
docker-compose up -d
```

**Local Development (see SETUP.md):**
```bash
# Terminal 1 - Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2 - Worker
cd worker && python worker.py

# Terminal 3 - Frontend
cd frontend && npm run dev
```

## 📡 API Usage

### Upload Audio
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@audio.mp3" \
  -F "diarization=true"

# Response
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "audio.mp3",
  "diarization_enabled": true,
  "message": "File uploaded successfully"
}
```

### Check Status
```bash
curl http://localhost:8000/jobs/550e8400-e29b-41d4-a716-446655440000/status
```

### Get Result
```bash
curl http://localhost:8000/jobs/550e8400-e29b-41d4-a716-446655440000/result
```

See [API.md](API.md) for complete API documentation.

## 🐳 Docker Hub Images

Pre-built images are available on Docker Hub under `trashcluster`:

```bash
docker pull trashcluster/otis-backend:latest
docker pull trashcluster/otis-worker:latest
docker pull trashcluster/otis-frontend:latest
```

Docker Compose automatically uses these images. To build locally:

```bash
# Uncomment build sections in docker-compose.yml
# Or rebuild specific service
docker-compose build backend
```

## 🔄 Workflow

1. User uploads audio file via UI or API
2. File stored in MinIO/S3
3. Job created in PostgreSQL with status "queued"
4. Backend enqueues transcription job to Redis
5. Worker picks up job and sends to OpenAI API
6. Worker stores result in S3 and updates job status
7. Frontend polls for completion and displays result

### Supported Formats
- WAV
- MP3
- M4A
- FLAC
- OGG
- **Max file size**: 500MB

### Transcription Models

**With Diarization:**
- Model: `gpt-4o-transcribe-diarize`
- Returns: Speaker-labeled segments with timestamps

**Without Diarization:**
- Model: `gpt-4o-mini-transcribe`
- Returns: Plain text transcript

## 🛡️ Security Features

- File size validation (500MB limit)
- MIME type validation
- Non-root Docker containers
- Environment-based secrets
- CORS middleware enabled
- SQL injection protection (SQLAlchemy ORM)

## 📊 Monitoring & Logging

- Structured logging (all services)
- Health checks on all containers
- Database indexes for performance
- Redis job queue monitoring (RQ dashboard available)

## 🚀 Production Deployment

### Kubernetes Ready
Docker images are compatible with Kubernetes. Add:
- Ingress controller for routing
- Persistent volumes for data
- ConfigMaps for configuration
- Secrets for API keys & credentials

### Scale Workers
```bash
docker-compose up -d --scale worker=3
```

### Monitor with Logs
```bash
docker-compose logs -f backend worker
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Submit pull request

## 📝 Key Improvements from Base Requirements

✅ **Multi-stage Docker builds** - Optimized image sizes
✅ **Non-root containers** - Enhanced security
✅ **Health checks** - Automatic service monitoring
✅ **Error handling** - Comprehensive exception handling & retry logic
✅ **Production configuration** - Environment-based secrets
✅ **Type safety** - Full TypeScript & Python type hints
✅ **Documentation** - API docs, setup guide, README

## 📄 License

MIT - See LICENSE file

## 🙋 Support

- **API Documentation**: See [API.md](API.md)
- **Setup Guide**: See [SETUP.md](SETUP.md)
- **Requirements**: See [PROMPT.md](PROMPT.md)

---

**Built with ❤️ by trashcluster for production-grade audio transcription**
