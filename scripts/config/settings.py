"""Configuration settings management"""

from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


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

    # Directory Configuration
    output_directory: str = Field(
        default="./notes",
        description="Directory to save generated notes"
    )

    temp_directory: str = Field(
        default="./temp",
        description="Temporary directory for processing files"
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

    chunk_size: int = Field(
        default=25 * 1024 * 1024,  # 25MB
        description="Chunk size for processing large files"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        Path(self.temp_directory).mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
