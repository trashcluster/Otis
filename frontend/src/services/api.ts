import axios, { AxiosInstance } from 'axios';

export interface UploadResponse {
  job_id: string;
  filename: string;
  diarization_enabled: boolean;
  message: string;
}

export interface JobStatus {
  job_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
}

export interface JobResult {
  status: string;
  job_id: string;
  filename: string;
  diarization_enabled: boolean;
  transcript: any;
  completed_at?: string;
  error?: string;
}

const API_BASE_URL = '/api';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

export const apiService = {
  uploadFile: async (file: File, diarization: boolean): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('diarization', String(diarization));

    const response = await api.post<UploadResponse>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getJobStatus: async (jobId: string): Promise<JobStatus> => {
    const response = await api.get<JobStatus>(`/jobs/${jobId}/status`);
    return response.data;
  },

  getJobResult: async (jobId: string): Promise<JobResult> => {
    const response = await api.get<JobResult>(`/jobs/${jobId}/result`);
    return response.data;
  },

  healthCheck: async (): Promise<any> => {
    const response = await api.get('/health');
    return response.data;
  },
};
