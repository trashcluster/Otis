import React, { FC } from 'react';

interface Segment {
  speaker: string;
  start: number;
  end: number;
  text: string;
}

interface TranscriptViewerProps {
  transcript: any;
  diarization: boolean;
}

export const TranscriptViewer: FC<TranscriptViewerProps> = ({ transcript, diarization }) => {
  if (!transcript) return null;

  if (diarization && transcript.segments && Array.isArray(transcript.segments)) {
    return (
      <div className="bg-white rounded-lg shadow p-6 max-w-2xl mx-auto mt-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Transcript</h2>
        <div className="space-y-4">
          {transcript.segments.map((segment: Segment, idx: number) => (
            <div key={idx} className="transcript-segment bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <span className="speaker-badge">{segment.speaker}</span>
                <span className="text-xs text-gray-500">
                  {segment.start.toFixed(1)}s - {segment.end.toFixed(1)}s
                </span>
              </div>
              <p className="text-gray-700 text-base">{segment.text}</p>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Standard transcript
  return (
    <div className="bg-white rounded-lg shadow p-6 max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Transcript</h2>
      <p className="text-gray-700 text-lg leading-relaxed whitespace-pre-wrap">
        {transcript.text}
      </p>
    </div>
  );
};
