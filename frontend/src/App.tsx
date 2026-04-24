import React, { useEffect, useState } from 'react';
import { FileUploader } from './components/FileUploader';
import { JobStatusDisplay } from './components/JobStatus';
import { TranscriptViewer } from './components/TranscriptViewer';
import { apiService, JobStatus, JobResult } from './services/api';
import './index.css';

type AppStage = 'upload' | 'processing' | 'result';

const App: React.FC = () => {
  const [stage, setStage] = useState<AppStage>('upload');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [diarizationEnabled, setDiarizationEnabled] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
  const [jobResult, setJobResult] = useState<JobResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Poll for job status
  useEffect(() => {
    if (stage !== 'processing' || !jobId) return;

    const interval = setInterval(async () => {
      try {
        const status = await apiService.getJobStatus(jobId);
        setJobStatus(status);

        if (status.status === 'completed') {
          const result = await apiService.getJobResult(jobId);
          setJobResult(result);
          setStage('result');
          setLoading(false);
        } else if (status.status === 'failed') {
          setError('Job processing failed');
          setStage('result');
          setLoading(false);
        }
      } catch (err) {
        console.error('Error checking job status:', err);
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, [stage, jobId]);

  const handleFileUpload = async (file: File, diarization: boolean) => {
    setLoading(true);
    setError(null);
    setUploadedFile(file);
    setDiarizationEnabled(diarization);

    try {
      const response = await apiService.uploadFile(file, diarization);
      setJobId(response.job_id);
      setStage('processing');
      setJobStatus({ job_id: response.job_id, status: 'queued' });
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Upload failed';
      setError(errorMsg);
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStage('upload');
    setUploadedFile(null);
    setDiarizationEnabled(false);
    setJobId(null);
    setJobStatus(null);
    setJobResult(null);
    setLoading(false);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-2">🎙️ Otis</h1>
          <p className="text-xl text-gray-600">Audio Transcription with Speaker Diarization</p>
        </div>

        {/* Main Content */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-4 rounded mb-6 max-w-md mx-auto">
            <p className="font-bold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {stage === 'upload' && <FileUploader onUpload={handleFileUpload} uploading={loading} />}

        {stage === 'processing' && jobStatus && (
          <>
            <JobStatusDisplay jobStatus={jobStatus} isLoading={true} />
            <div className="mt-8 text-center">
              <p className="text-sm text-gray-600">Processing: {uploadedFile?.name}</p>
            </div>
          </>
        )}

        {stage === 'result' && jobResult && (
          <>
            <JobStatusDisplay jobStatus={{ job_id: jobResult.job_id, status: jobResult.status as any }} />
            {jobResult.status === 'completed' && (
              <TranscriptViewer transcript={jobResult.transcript} diarization={diarizationEnabled} />
            )}
            {jobResult.status === 'failed' && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-4 rounded mt-8 max-w-md mx-auto">
                <p className="font-bold">Processing Failed</p>
                <p>{jobResult.error || 'Unknown error'}</p>
              </div>
            )}
          </>
        )}

        {/* Reset Button */}
        {stage !== 'upload' && (
          <div className="text-center mt-8">
            <button
              onClick={handleReset}
              className="px-8 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-all"
            >
              Upload Another File
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
