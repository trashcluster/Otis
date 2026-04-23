You are a senior full-stack engineer and cloud architect.

Your task is to generate a production-ready web application that allows users to upload audio files, process them asynchronously, and return transcriptions with optional speaker diarization.

The system must be modular, scalable, and cloud-friendly.

---

# OVERVIEW

Build a web application that:

1. Accepts audio file uploads via drag-and-drop.
2. Stores uploaded files in an S3-compatible object storage.
3. Places transcription jobs into a queue.
4. Processes jobs asynchronously using OpenAI transcription APIs.
5. Supports optional speaker diarization.
6. Stores transcripts and metadata.
7. Displays job status and results in the UI.

---

# CORE FEATURES

## Frontend

Build a modern web UI with:

* Drag-and-drop audio upload
* File selection button
* Toggle option:

  * "Enable Speaker Diarization"
* Upload progress indicator
* Job status display:

  * queued
  * processing
  * completed
  * failed
* Transcript viewer
* Speaker-labeled transcript view (if diarization enabled)

Use:

* React
* TypeScript
* TailwindCSS
* Axios for API calls

---

## Backend API

Build a REST API with:

* FastAPI (Python)

Endpoints:

POST /upload

* Accept audio file
* Accept diarization boolean
* Store file to S3
* Create job entry
* Push job to queue
* Return job_id

GET /jobs/{job_id}

* Return job status

GET /jobs/{job_id}/result

* Return transcript data

---

## Storage

Use:

* S3-compatible storage

Requirements:

* Store raw uploaded audio
* Store processed transcript JSON
* Use structured key layout:

uploads/{job_id}/audio.ext
results/{job_id}/transcript.json

---

## Job Queue

Use:

* Redis
* RQ or Celery workers

Requirements:

* Upload endpoint pushes jobs into queue
* Worker consumes jobs
* Worker processes transcription
* Worker updates job status

Job states:

* queued
* processing
* completed
* failed

---

# TRANSCRIPTION ENGINE

Use OpenAI transcription APIs.

## With Diarization Enabled

Use:

gpt-4o-transcribe-diarize

Requirements:

* Enable speaker diarization
* Return speaker-labeled transcript
* Store transcript JSON

Expected output format:

{
"segments": [
{
"speaker": "Speaker 1",
"start": 0.0,
"end": 3.2,
"text": "Hello world"
}
]
}

---

## Without Diarization

Use:

gpt-4o-mini-transcribe

Requirements:

* Return standard transcript
* Store transcript JSON

Expected output:

{
"text": "Full transcript text"
}

---

# DATABASE

Use:

PostgreSQL

Table: jobs

Columns:

* id (UUID)
* filename
* s3_key
* diarization_enabled (boolean)
* status
* created_at
* completed_at
* error_message

---

# WORKER LOGIC

Worker must:

1. Fetch job from queue
2. Download file from S3
3. Select model:

IF diarization_enabled == true
→ use gpt-4o-transcribe-diarize

ELSE
→ use gpt-4o-mini-transcribe

4. Send audio to OpenAI API
5. Store result JSON to S3
6. Update job status
7. Handle retry logic
8. Log failures

---

# FILE SUPPORT

Accept:

* wav
* mp3
* m4a
* flac
* ogg

Reject unsupported types.

Max file size:

500 MB

---

# SECURITY

Implement:

* File size validation
* MIME type validation
* Signed S3 uploads (optional improvement)
* API rate limiting
* Environment-based secrets

---

# INFRASTRUCTURE

Use Docker for all services.

Provide:

* Dockerfiles for `frontend`, `backend`, and `worker` (multi-stage, non-root, production-ready)
* docker-compose.yml (production and local development friendly)
* .dockerignore files for each Dockerized component

Services:

* frontend
* backend
* worker
* redis
* postgres
* minio (for local S3 testing)

Container Images (Docker Hub):

* Use Docker Hub autobuilt images under the user `trashcluster`.
* Image names:
  * `trashcluster/otis-frontend`
  * `trashcluster/otis-backend`
  * `trashcluster/otis-worker`
* docker-compose must reference these images by default using a configurable tag:
  * frontend: `trashcluster/otis-frontend:${IMAGE_TAG:-latest}`
  * backend: `trashcluster/otis-backend:${IMAGE_TAG:-latest}`
  * worker: `trashcluster/otis-worker:${IMAGE_TAG:-latest}`
* Provide an easy local-build option (compose profiles or commented `build:` blocks) to override images with local builds when needed, without changing defaults.

---

# CONFIGURATION

Use environment variables:

OPENAI_API_KEY
S3_ENDPOINT
S3_ACCESS_KEY
S3_SECRET_KEY
S3_BUCKET
REDIS_URL
DATABASE_URL
IMAGE_TAG (default: latest)

---

# FRONTEND UI DETAILS

Home Page:

* Drag-and-drop upload zone
* Checkbox:

[ ] Enable Speaker Diarization

* Upload button

Jobs Page:

Table:

* Job ID
* Filename
* Status
* Created time
* View Result button

Result Page:

If diarization:

Display:

Speaker 1: Hello
Speaker 2: Hi

Else:

Display:

Full transcript text

---

# ERROR HANDLING

Implement:

* Retry failed jobs (3 times)
* Store failure reason
* Display error in UI

---

# OUTPUT FORMAT

Generate:

1. Full project structure
2. Backend source code
3. Frontend source code
4. Worker code
5. Docker configuration (Dockerfiles and docker-compose.yml referencing `trashcluster/*` images by default)
6. Database schema
7. Example .env file
8. Setup instructions
9. API documentation
10. Example requests

---

# CODING REQUIREMENTS

* Use type-safe code
* Use logging
* Use modular structure
* Write clear comments
* Follow production best practices

---

# OPTIONAL ENHANCEMENTS (if time allows)

* Authentication system
* WebSocket job updates
* Transcript search
* Speaker coloring
* Export transcript as:

  * TXT
  * JSON
  * SRT
  * VTT

---

Begin generating the full implementation now.
