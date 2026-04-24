import React, { useState, useRef } from 'react';

interface UploaderProps {
  onUpload: (file: File, diarization: boolean) => void;
  uploading?: boolean;
}

export const FileUploader: React.FC<UploaderProps> = ({ onUpload, uploading = false }) => {
  const [dragOver, setDragOver] = useState(false);
  const [diarization, setDiarization] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onUpload(files[0], diarization);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(e.target.files[0], diarization);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileSelect}
          className="hidden"
          disabled={uploading}
        />
        <div className="text-6xl mb-4">🎵</div>
        <p className="text-xl font-semibold text-gray-700 mb-2">
          {uploading ? 'Uploading...' : 'Drag & drop audio file here'}
        </p>
        <p className="text-gray-500 mb-4">or click to select</p>
        <p className="text-sm text-gray-400">
          Supported: WAV, MP3, M4A, FLAC, OGG (Max 500MB)
        </p>
      </div>

      <div className="mt-6 flex items-center space-x-2">
        <input
          type="checkbox"
          id="diarization"
          checked={diarization}
          onChange={(e) => setDiarization(e.target.checked)}
          className="w-4 h-4 rounded border-gray-300"
          disabled={uploading}
        />
        <label htmlFor="diarization" className="text-sm font-medium text-gray-700">
          Enable Speaker Diarization
        </label>
      </div>

      <button
        onClick={handleClick}
        disabled={uploading}
        className="mt-6 w-full px-6 py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all"
      >
        {uploading ? 'Uploading...' : 'Upload Audio'}
      </button>
    </div>
  );
};
