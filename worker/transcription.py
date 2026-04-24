"""Transcription processing with OpenAI."""
import logging
import json
import tempfile
from typing import Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def transcribe_with_diarization(file_path: str) -> Optional[dict]:
    """Transcribe audio with speaker diarization."""
    try:
        logger.info(f"Transcribing with diarization: {file_path}")
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe-diarize",
                file=audio_file,
                response_format="verbose_json",
            )
        
        # Format response
        if hasattr(transcript, 'segments'):
            return {
                "segments": [
                    {
                        "speaker": seg.get("speaker", "Unknown"),
                        "start": seg.get("start", 0.0),
                        "end": seg.get("end", 0.0),
                        "text": seg.get("text", ""),
                    }
                    for seg in transcript.segments
                ]
            }
        else:
            # Fallback to standard transcript
            return {
                "text": transcript.text if hasattr(transcript, 'text') else str(transcript),
                "segments": []
            }
    except Exception as e:
        logger.error(f"Diarization error: {e}")
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def transcribe_standard(file_path: str) -> Optional[dict]:
    """Transcribe audio without speaker diarization."""
    try:
        logger.info(f"Transcribing standard: {file_path}")
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
                response_format="json",
            )
        
        # Format response
        return {
            "text": transcript.text if hasattr(transcript, 'text') else str(transcript),
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise


def process_audio(file_path: str, diarization_enabled: bool) -> Optional[dict]:
    """Process audio file for transcription."""
    try:
        if diarization_enabled:
            return transcribe_with_diarization(file_path)
        else:
            return transcribe_standard(file_path)
    except Exception as e:
        logger.error(f"Audio processing failed: {e}")
        raise
