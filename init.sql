# Database initialization script
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(512) NOT NULL UNIQUE,
    diarization_enabled BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'queued' NOT NULL CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
