"""Speech-to-text transcription module using local OpenAI Whisper"""

import asyncio
from pathlib import Path
from typing import Dict, Optional
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import whisper
except ImportError:
    raise ImportError(
        "OpenAI Whisper is required. Install it with: pip install openai-whisper"
    )

from config.settings import get_settings
from core.exceptions import TranscriptionError

logger = logging.getLogger(__name__)


class Transcriber:
    """Handles speech-to-text transcription using local Whisper model"""

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize transcriber with specified Whisper model

        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
                        If None, uses value from settings
        """
        self.settings = get_settings()
        self.model_name = model_name or self.settings.whisper_model
        self._model = None

        logger.info(f"Transcriber initialized with model: {self.model_name}")

    @property
    def model(self):
        """Lazy load Whisper model"""
        if self._model is None:
            try:
                logger.info(f"Loading Whisper model: {self.model_name}")
                self._model = whisper.load_model(self.model_name)
                logger.info(f"Whisper model {self.model_name} loaded successfully")
            except Exception as e:
                raise TranscriptionError(
                    f"Failed to load Whisper model {self.model_name}: {str(e)}"
                )
        return self._model

    async def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio file to text (async to avoid blocking)

        Args:
            audio_path: Path to audio file
            language: Source language code (e.g., 'zh', 'en'). If None, auto-detect

        Returns:
            Dictionary containing transcription result:
            {
                'text': 'full transcription text',
                'language': 'detected language code',
                'segments': [...],  # detailed segments (optional)
                'duration': duration_in_seconds
            }

        Raises:
            TranscriptionError: If transcription fails
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise TranscriptionError(f"Audio file not found: {audio_path}")

        if audio_path.suffix.lower() not in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
            raise TranscriptionError(f"Unsupported audio format: {audio_path.suffix}")

        try:
            # Prepare transcription options
            options = {
                'task': 'transcribe',
                'fp16': False,  # Disable FP16 for compatibility
                'verbose': False,
            }

            # Add language if specified
            if language:
                options['language'] = language

            # Perform transcription in thread pool to avoid blocking event loop
            logger.info(f"Starting transcription of {audio_path.name} using model {self.model_name}...")

            # Run Whisper in a thread pool to avoid blocking
            result = await asyncio.to_thread(
                self.model.transcribe,
                str(audio_path),
                **options
            )

            # Process the result
            processed_result = {
                'text': result.get('text', '').strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'duration': result.get('segments', [])[-1].get('end', 0) if result.get('segments') else 0
            }

            logger.info(
                f"Transcription completed. "
                f"Duration: {processed_result['duration']:.2f}s, "
                f"Language: {processed_result['language']}, "
                f"Text length: {len(processed_result['text'])} characters"
            )

            return processed_result

        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}", exc_info=True)
            raise TranscriptionError(f"Transcription failed: {str(e)}")

    def detect_language(self, result: dict) -> str:
        """
        Extract detected language from transcription result

        Args:
            result: Transcription result dictionary

        Returns:
            Language code (e.g., 'zh', 'en')
        """
        return result.get('language', 'unknown')

    def get_full_text(self, result: dict) -> str:
        """
        Extract full transcription text from result

        Args:
            result: Transcription result dictionary

        Returns:
            Full transcription text
        """
        return result.get('text', '').strip()
