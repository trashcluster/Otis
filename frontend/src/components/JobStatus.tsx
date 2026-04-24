import React from 'react';
import { JobStatus } from '../services/api';

interface JobStatusDisplayProps {
  jobStatus: JobStatus | null;
  isLoading?: boolean;
}

export const JobStatusDisplay: React.FC<JobStatusDisplayProps> = ({ jobStatus, isLoading = false }) => {
  if (!jobStatus) return null;

  const statusColors: Record<string, string> = {
    queued: 'bg-yellow-100 text-yellow-800',
    processing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const statusIcons: Record<string, string> = {
    queued: '⏳',
    processing: '🔄',
    completed: '✅',
    failed: '❌',
  };

  const statusColor = statusColors[jobStatus.status] || statusColors.queued;
  const statusIcon = statusIcons[jobStatus.status] || '❓';

  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-md mx-auto mt-8">
      <div className="flex items-center space-x-4">
        <div className="text-4xl">{statusIcon}</div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-700">Job Status</h3>
          <p className="text-sm text-gray-500 mt-1">ID: {jobStatus.job_id}</p>
          <div className={`inline-block mt-3 px-4 py-2 rounded-full font-semibold text-sm ${statusColor}`}>
            {jobStatus.status.toUpperCase()}
          </div>
        </div>
      </div>
      {isLoading && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-500 h-2 rounded-full animate-pulse"></div>
          </div>
        </div>
      )}
    </div>
  );
};
