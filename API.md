# Otis API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. Consider implementing API keys for production.

## Endpoints

### Health Check
```
GET /health
```

**Response (200)**
```json
{
  "status": "ok"
}
```

---

### Upload Audio File
```
POST /upload
```

**Request**
- `Content-Type`: `multipart/form-data`
- Parameters:
  - `file` (required): Audio file (wav, mp3, m4a, flac, ogg) - Max 500MB
  - `diarization` (optional): Boolean, enable speaker diarization (default: false)

**Example Request**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@audio.mp3" \
  -F "diarization=true"
```

**Response (200)**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "audio.mp3",
  "diarization_enabled": true,
  "message": "File uploaded successfully"
}
```

**Error Responses**
- `400`: Invalid file type
- `413`: File too large
- `500`: Server error

---

### Get Job Status
```
GET /jobs/{job_id}/status
```

**Example Request**
```bash
curl http://localhost:8000/jobs/550e8400-e29b-41d4-a716-446655440000/status
```

**Response (200)**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing"
}
```

**Status Values**
- `queued`: Waiting to be processed
- `processing`: Currently being transcribed
- `completed`: Successfully completed
- `failed`: Processing failed

---

### Get Job Details
```
GET /jobs/{job_id}
```

**Response (200)**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "audio.mp3",
  "s3_key": "uploads/abc123/audio.mp3",
  "diarization_enabled": true,
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:35:00",
  "error_message": null
}
```

---

### Get Transcription Result
```
GET /jobs/{job_id}/result
```

**Response (200) - With Diarization**
```json
{
  "status": "completed",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "audio.mp3",
  "diarization_enabled": true,
  "transcript": {
    "segments": [
      {
        "speaker": "Speaker 1",
        "start": 0.0,
        "end": 3.2,
        "text": "Hello, how are you?"
      },
      {
        "speaker": "Speaker 2",
        "start": 3.5,
        "end": 6.1,
        "text": "I'm doing great, thanks for asking."
      }
    ]
  },
  "completed_at": "2024-01-15T10:35:00"
}
```

**Response (200) - Without Diarization**
```json
{
  "status": "completed",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "audio.mp3",
  "diarization_enabled": false,
  "transcript": {
    "text": "Hello, how are you? I'm doing great, thanks for asking."
  },
  "completed_at": "2024-01-15T10:35:00"
}
```

**Response (202) - Processing**
```json
{
  "status": "processing",
  "message": "Job is still processing"
}
```

**Response (200) - Failed**
```json
{
  "status": "failed",
  "error": "Failed to process audio file"
}
```

---

## Example Workflow

1. **Upload file**
```bash
JOB_ID=$(curl -s -X POST http://localhost:8000/upload \
  -F "file=@sample.mp3" \
  -F "diarization=true" | jq -r '.job_id')
```

2. **Check status (poll)**
```bash
curl http://localhost:8000/jobs/$JOB_ID/status
```

3. **Get result when completed**
```bash
curl http://localhost:8000/jobs/$JOB_ID/result | jq '.transcript'
```

---

## Error Handling

All errors include a JSON response with `detail` field:

```json
{
  "detail": "File type not allowed. Allowed types: wav, mp3, m4a, flac, ogg"
}
```

Common errors:
- `400 Bad Request`: Invalid input
- `404 Not Found`: Job not found
- `413 Payload Too Large`: File exceeds 500MB
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Currently not implemented. Consider adding for production workloads.

---

## Pagination

Currently not implemented. Single job queries only.
