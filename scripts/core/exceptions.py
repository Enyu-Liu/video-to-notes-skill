"""Custom exceptions for video processing"""


class VideoNoteError(Exception):
    """Base exception for video-note-mcp"""
    pass


class VideoDownloadError(VideoNoteError):
    """Raised when video download fails"""
    pass


class AudioExtractionError(VideoNoteError):
    """Raised when audio extraction fails"""
    pass


class TranscriptionError(VideoNoteError):
    """Raised when speech transcription fails"""
    pass


class SummarizationError(VideoNoteError):
    """Raised when AI summarization fails"""
    pass


class FileOperationError(VideoNoteError):
    """Raised when file operations fail"""
    pass


class ConfigurationError(VideoNoteError):
    """Raised when configuration is invalid"""
    pass
