"""Video downloading and audio extraction module"""

import os
import shutil
from pathlib import Path
from typing import Optional, Tuple
import yt_dlp
from datetime import timedelta
import logging
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import get_settings
from core.exceptions import VideoDownloadError, AudioExtractionError

logger = logging.getLogger(__name__)

# Create a dedicated thread pool for ffmpeg to avoid conflicts
_ffmpeg_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="ffmpeg_")


class VideoProcessor:
    """Handles video downloading and audio extraction"""

    def __init__(self):
        self.settings = get_settings()
        self.temp_dir = Path(self.settings.temp_directory)

    def download_video(self, url: str) -> Tuple[str, dict]:
        """
        Download video from URL and return video path and metadata

        Args:
            url: Video URL (bilibili or youtube)

        Returns:
            Tuple of (video_path, metadata)

        Raises:
            VideoDownloadError: If download fails
        """
        # Custom logger to redirect yt-dlp output to stderr
        class YtdlpLogger:
            def debug(self, msg):
                if msg.startswith('[debug] '):
                    logger.debug(msg)
                else:
                    logger.info(msg)

            def info(self, msg):
                logger.info(msg)

            def warning(self, msg):
                logger.warning(msg)

            def error(self, msg):
                logger.error(msg)

        # Configure download options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'noplaylist': True,
            'quiet': True,  # Suppress console output
            'no_warnings': True,  # Suppress warnings to stdout
            'logger': YtdlpLogger(),  # Use custom logger that writes to stderr
            'socket_timeout': 60,  # Increase timeout to 60 seconds
            'retries': 3,  # Retry 3 times on failure
            'fragment_retries': 3,  # Retry fragments
            'noresizebuffer': True,  # Don't use resume
            'http_chunk_size': 10485760,  # 10MB chunks
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get metadata
                info = ydl.extract_info(url, download=False)

                # Check video duration
                duration = info.get('duration', 0)
                if duration > self.settings.max_video_length:
                    raise VideoDownloadError(
                        f"Video too long: {duration}s > {self.settings.max_video_length}s"
                    )

                # Download the video
                ydl.download([url])

                # Get the downloaded file path
                video_path = Path(ydl.prepare_filename(info))
                if not video_path.exists():
                    # Sometimes extension changes, find the actual file
                    base_path = video_path.with_suffix('')
                    for ext in ['.mp4', '.mkv', '.webm', '.avi']:
                        candidate = base_path.with_suffix(ext)
                        if candidate.exists():
                            video_path = candidate
                            break

                if not video_path.exists():
                    raise VideoDownloadError("Downloaded video file not found")

                # Prepare metadata
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': duration,
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'url': url,
                    'id': info.get('id', ''),
                    'platform': 'youtube' if 'youtube' in url else 'bilibili'
                }

                return str(video_path), metadata

        except Exception as e:
            raise VideoDownloadError(f"Failed to download video: {str(e)}")

    async def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video file (async to avoid blocking)

        Args:
            video_path: Path to video file

        Returns:
            Path to extracted audio file

        Raises:
            AudioExtractionError: If extraction fails
        """
        import asyncio
        import subprocess

        video_path = Path(video_path)
        if not video_path.exists():
            raise AudioExtractionError(f"Video file not found: {video_path}")

        # Generate output audio path
        audio_path = self.temp_dir / f"{video_path.stem}.mp3"

        try:
            video_size_mb = video_path.stat().st_size / (1024*1024)
            logger.info(f"Starting audio extraction: {video_path.name}")
            logger.info(f"Video size: {video_size_mb:.2f} MB")

            # Check if video is unusually large
            if video_size_mb > 500:
                logger.warning(f"⚠️  Large video file ({video_size_mb:.1f} MB) - extraction may be slow")

            # Build ffmpeg command - optimized for speed
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-b:a', '64k',  # Lower bitrate for faster processing
                '-ac', '1',  # Mono for Whisper
                '-ar', '16000',  # 16kHz for Whisper
                '-y',  # Overwrite
                str(audio_path)
            ]

            logger.debug(f"FFmpeg command: {' '.join(cmd[:10])}...")

            # CRITICAL FIX: Use asyncio native subprocess instead of thread pool
            # subprocess.run hangs in MCP context, but asyncio.create_subprocess works
            logger.debug("Creating async subprocess for ffmpeg...")

            import time
            start = time.time()

            # Create async subprocess - use CREATE_NO_WINDOW on Windows
            try:
                # On Windows, prevent console window from appearing
                if os.name == 'nt':
                    creation_flags = subprocess.CREATE_NO_WINDOW
                else:
                    creation_flags = 0

                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                    creationflags=creation_flags
                )

                logger.debug(f"Subprocess created (pid={process.pid}), waiting for completion...")

                # Wait for process to complete
                returncode = await asyncio.wait_for(
                    process.wait(),
                    timeout=30  # 30 seconds should be plenty
                )

                elapsed = time.time() - start
                logger.debug(f"FFmpeg completed in {elapsed:.2f}s, returncode={returncode}")

            except asyncio.TimeoutError:
                # Kill the process if it times out
                try:
                    process.kill()
                    await process.wait()
                except:
                    pass
                logger.error(f"FFmpeg timed out after 30 seconds")
                raise AudioExtractionError("FFmpeg process timed out after 30 seconds")
            except Exception as e:
                logger.error(f"FFmpeg subprocess error: {e}")
                raise AudioExtractionError(f"Failed to run ffmpeg: {str(e)}")

            # Check if ffmpeg succeeded
            if returncode != 0:
                logger.error(f"FFmpeg failed with returncode {returncode}")
                raise AudioExtractionError(f"FFmpeg failed with exit code {returncode}")

            # Check if output file was created
            if not audio_path.exists():
                logger.error("Audio extraction failed - output file not created")
                raise AudioExtractionError("Audio extraction failed - output file not created")

            # Success!
            audio_size = audio_path.stat().st_size / (1024*1024)
            elapsed_total = time.time() - start
            logger.info(f"Audio extraction completed: {audio_path.name} ({audio_size:.2f} MB) in {elapsed_total:.2f}s")
            return str(audio_path)

        except AudioExtractionError:
            raise
        except Exception as e:
            logger.error(f"Audio extraction error: {str(e)}", exc_info=True)
            raise AudioExtractionError(f"Failed to extract audio: {str(e)}")

    def cleanup_temp_files(self, *file_paths: str) -> None:
        """
        Clean up temporary files

        Args:
            *file_paths: Variable arguments of file paths to clean up
        """
        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists():
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
            except Exception as e:
                # Log error but don't raise as cleanup should not stop processing
                logger.warning(f"Failed to cleanup {file_path}: {str(e)}")

    def get_video_info(self, url: str) -> dict:
        """
        Get video information without downloading

        Args:
            url: Video URL

        Returns:
            Video metadata dictionary
        """
        # Custom logger to redirect yt-dlp output to stderr
        class YtdlpLogger:
            def debug(self, msg):
                logger.debug(msg)
            def info(self, msg):
                logger.info(msg)
            def warning(self, msg):
                logger.warning(msg)
            def error(self, msg):
                logger.error(msg)

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'logger': YtdlpLogger(),  # Use custom logger
            'skip_download': True,
            'socket_timeout': 60,  # Increase timeout to 60 seconds
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'description': info.get('description', '')[:500],  # Truncate long descriptions
                    'upload_date': info.get('upload_date', ''),
                    'url': url,
                    'id': info.get('id', ''),
                    'platform': 'youtube' if 'youtube' in url else 'bilibili',
                    'duration_formatted': str(timedelta(seconds=info.get('duration', 0)))
                }
        except Exception as e:
            raise VideoDownloadError(f"Failed to get video info: {str(e)}")
