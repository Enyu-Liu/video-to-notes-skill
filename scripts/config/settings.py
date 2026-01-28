"""Configuration settings management"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

# Get the absolute path to the scripts directory
SCRIPTS_DIR = Path(__file__).parent.parent.absolute()


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    openrouter_api_key: str = Field(
        default="",
        description="OpenRouter API key for AI model access"
    )

    # Whisper Configuration
    whisper_model: str = Field(
        default="base",
        description="Whisper model size: tiny, base, small, medium, large"
    )

    # AI Model Configuration
    ai_model: str = Field(
        default="anthropic/claude-3.5-sonnet",
        description="AI model to use for summarization"
    )

    # Language Configuration
    default_language: str = Field(
        default="zh",
        description="Default language for transcription and summarization (zh/en/ja/ko/es/fr/de/auto)"
    )

    # Directory Configuration
    output_directory: str = Field(
        default=".",
        description="Directory to save generated notes (default: current directory)"
    )

    temp_directory: str = Field(
        default=str(SCRIPTS_DIR / "temp"),
        description="Temporary directory for processing files (created automatically when needed, always in skill folder)"
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    # Processing Configuration
    max_video_length: int = Field(
        default=7200,  # 2 hours in seconds
        description="Maximum video length in seconds to process"
    )

    # YouTube Authentication
    youtube_cookies: str = Field(
        default="",
        description="Path to cookies.txt file for YouTube authentication (bypass bot detection)"
    )

    chunk_size: int = Field(
        default=25 * 1024 * 1024,  # 25MB
        description="Chunk size for processing large files"
    )

    # API Parameters Configuration
    max_tokens: int = Field(
        default=5000,
        description="Maximum tokens for AI model response (used by summarizer for API calls)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Note: Directories are created on-demand when actually needed
        # This avoids creating unnecessary folders in the current directory


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
