"""YouTube transcript fetching module using youtube-transcript-api

This module provides an alternative to downloading videos and using Whisper.
It fetches transcripts directly from YouTube's caption system.
"""

import logging
from typing import Optional, Dict, List, Tuple
from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger(__name__)


class YouTubeTranscriptFetcher:
    """Fetches transcripts directly from YouTube"""

    def __init__(self):
        self.api = YouTubeTranscriptApi()

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL

        Args:
            url: YouTube URL

        Returns:
            Video ID or None if not a valid YouTube URL
        """
        import re

        # Pattern for various YouTube URL formats
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def list_available_transcripts(self, video_id: str) -> List[Dict]:
        """
        List available transcripts for a video

        Args:
            video_id: YouTube video ID

        Returns:
            List of transcript info dictionaries
        """
        try:
            transcript_list = self.api.list(video_id)
            return [
                {
                    'language': t.language,
                    'language_code': t.language_code,
                    'is_generated': t.is_generated,
                    'is_translatable': t.is_translatable,
                }
                for t in transcript_list
            ]
        except Exception as e:
            logger.error(f"Failed to list transcripts: {e}")
            return []

    def fetch_transcript(
        self,
        video_id: str,
        language: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Fetch transcript for a video

        Args:
            video_id: YouTube video ID
            language: Preferred language code (e.g., 'en', 'zh')

        Returns:
            Tuple of (transcript_text, detected_language)

        Raises:
            Exception: If transcript fetching fails
        """
        try:
            # Try to fetch transcript with specified language or auto-detect
            if language:
                try:
                    transcript = self.api.fetch(video_id, languages=[language])
                    detected_lang = language
                except Exception:
                    logger.info(f"Transcript not available in {language}, trying default")
                    transcript = self.api.fetch(video_id)
                    detected_lang = self._detect_language_from_transcript(transcript)
            else:
                transcript = self.api.fetch(video_id)
                detected_lang = self._detect_language_from_transcript(transcript)

            # Convert segments to full text
            full_text = self._segments_to_text(transcript)

            logger.info(f"Fetched transcript: {len(transcript)} segments, {len(full_text)} characters")
            return full_text, detected_lang

        except Exception as e:
            logger.error(f"Failed to fetch transcript: {e}")
            raise

    def _segments_to_text(self, segments) -> str:
        """
        Convert transcript segments to full text

        Args:
            segments: List of transcript segments

        Returns:
            Full transcript text
        """
        # Join all segment texts with spaces
        text_parts = []
        for seg in segments:
            text = seg.text.strip()
            if text:
                text_parts.append(text)

        return ' '.join(text_parts)

    def _detect_language_from_transcript(self, segments) -> str:
        """
        Try to detect language from transcript content

        Args:
            segments: Transcript segments

        Returns:
            Detected language code
        """
        # Simple heuristic: check for Chinese characters
        sample_text = ' '.join([s.text for s in segments[:10]])

        # Check for Chinese characters
        chinese_chars = sum(1 for c in sample_text if '\u4e00' <= c <= '\u9fff')
        if chinese_chars > len(sample_text) * 0.1:
            return 'zh'

        # Default to English
        return 'en'


def fetch_youtube_transcript(url: str, language: Optional[str] = None) -> Tuple[str, str, dict]:
    """
    Convenience function to fetch YouTube transcript

    Args:
        url: YouTube video URL
        language: Preferred language code

    Returns:
        Tuple of (transcript_text, detected_language, metadata)
    """
    fetcher = YouTubeTranscriptFetcher()

    video_id = fetcher.extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    transcript_text, detected_lang = fetcher.fetch_transcript(video_id, language)

    # Return basic metadata
    metadata = {
        'video_id': video_id,
        'url': url,
        'transcript_source': 'youtube_captions',
    }

    return transcript_text, detected_lang, metadata
