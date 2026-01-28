"""Main script for processing videos and generating notes

This script can be used standalone or called by Claude Skills.
"""

import asyncio
import sys
import argparse
import logging
import os
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.video_processor import VideoProcessor
from core.summarizer import Summarizer
from core.exceptions import (
    VideoDownloadError,
    AudioExtractionError,
    TranscriptionError,
    SummarizationError,
    ConfigurationError
)
from config.settings import get_settings


# Configure logging to stderr (stdout is reserved for output)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


async def process_video(
    url: str,
    language: Optional[str] = None,
    ai_model: Optional[str] = None,
    save_to_file: bool = False,
    output_path: Optional[str] = None,
    local_video: Optional[str] = None,
    video_title: Optional[str] = None,
    cookies_file: Optional[str] = None,
    use_youtube_captions: bool = False
) -> str:
    """
    Process video and return markdown notes

    Args:
        url: Video URL (YouTube, Bilibili, or Xiaohongshu) - can be empty if local_video is provided
        language: Optional language code for transcription
        ai_model: Optional AI model override
        save_to_file: Whether to save output to file
        output_path: Optional output directory path
        local_video: Optional path to local video file (bypasses download)
        video_title: Optional video title (used with local_video)
        cookies_file: Optional path to cookies.txt file for YouTube authentication
        use_youtube_captions: Use YouTube's built-in captions instead of Whisper (faster, no download)

    Returns:
        Markdown formatted notes

    Raises:
        Various exceptions if processing fails
    """
    settings = get_settings()
    video_processor = VideoProcessor()

    # Use default language if not specified
    if not language:
        language = settings.default_language
        logger.info(f"Using default language: {language}")

    # Use cookies from settings if not provided via argument
    if not cookies_file and settings.youtube_cookies:
        cookies_file = settings.youtube_cookies
        logger.info(f"Using cookies from settings: {cookies_file}")

    # Initialize components
    try:
        # Use provided model or default from settings
        model_to_use = ai_model or settings.ai_model
        logger.info(f"Using AI model: {model_to_use}")
        summarizer = Summarizer(model=model_to_use)

        # Only initialize Whisper if not using YouTube captions
        transcriber = None
        if not use_youtube_captions:
            from core.transcriber import Transcriber
            transcriber = Transcriber()
            logger.info(f"Using local Whisper model: {settings.whisper_model}")
    except Exception as e:
        raise ConfigurationError(f"Failed to initialize components: {str(e)}")

    video_path = None
    audio_path = None
    is_local_video = False

    try:
        # Check if using YouTube captions (fast path - no download needed)
        if use_youtube_captions and url and ('youtube.com' in url or 'youtu.be' in url):
            logger.info("Using YouTube captions mode (fast, no download)")

            # Step 1: Get video metadata
            logger.info(f"Step 1/4: Fetching video metadata from {url}")
            try:
                metadata = video_processor.get_video_info(url, cookies_file=cookies_file)
                logger.info(f"✓ Video info: {metadata['title']}")
                logger.info(f"  Duration: {metadata.get('duration_formatted', 'Unknown')}")
            except Exception as e:
                # Fallback metadata
                logger.warning(f"Could not fetch video metadata: {e}")
                from core.youtube_transcript import YouTubeTranscriptFetcher
                video_id = YouTubeTranscriptFetcher.extract_video_id(url)
                metadata = {
                    'title': video_title or f'YouTube Video {video_id}',
                    'uploader': 'Unknown',
                    'duration': 0,
                    'description': '',
                    'upload_date': '',
                    'url': url,
                    'id': video_id or '',
                    'platform': 'youtube'
                }

            # Step 2: Fetch YouTube captions
            logger.info("Step 2/4: Fetching YouTube captions...")
            from core.youtube_transcript import fetch_youtube_transcript
            transcript_text, detected_language, _ = fetch_youtube_transcript(url, language)
            logger.info(f"✓ Captions fetched ({len(transcript_text)} characters, language: {detected_language})")

            # Skip to Step 3 (AI summary) - no download or Whisper needed

        else:
            # Standard path: Download video -> Extract audio -> Whisper transcription

            # Step 1: Download video or use local file
            if local_video:
                # Use local video file
                local_video_path = Path(local_video)
                if not local_video_path.exists():
                    raise VideoDownloadError(f"Local video file not found: {local_video}")

                logger.info(f"Step 1/6: Using local video file: {local_video_path.name}")
                video_path = str(local_video_path)
                is_local_video = True

                # Create metadata for local video
                metadata = {
                    'title': video_title or local_video_path.stem,
                    'uploader': 'Unknown',
                    'duration': 0,
                    'description': '',
                    'upload_date': '',
                    'url': url or f"local:{local_video}",
                    'id': local_video_path.stem,
                    'platform': 'local'
                }
                logger.info(f"✓ Using local video: {metadata['title']}")
            else:
                logger.info(f"Step 1/6: Downloading video from {url}")
                video_path, metadata = video_processor.download_video(url, cookies_file=cookies_file)
                logger.info(f"✓ Video downloaded: {metadata['title']}")
                logger.info(f"  Duration: {metadata.get('duration_formatted', 'Unknown')}")
                logger.info(f"  Platform: {metadata.get('platform', 'Unknown')}")

            # Step 2: Extract audio
            logger.info("Step 2/6: Extracting audio...")
            audio_path = await video_processor.extract_audio(video_path)
            logger.info(f"✓ Audio extracted: {Path(audio_path).name}")

            # Step 3: Transcribe audio
            logger.info(f"Step 3/6: Transcribing audio with local Whisper ({settings.whisper_model})...")
            transcription_result = await transcriber.transcribe(audio_path, language=language)
            transcript_text = transcription_result['text']
            detected_language = transcription_result['language']
            logger.info(f"✓ Transcription completed ({len(transcript_text)} characters, language: {detected_language})")

        # Step N: Generate AI summary (step 3/4 for YouTube captions, step 4/6 for standard)
        step_prefix = "Step 3/4" if use_youtube_captions else "Step 4/6"
        logger.info(f"{step_prefix}: Generating AI summary...")
        # Use detected language or specified language for summary
        summary_language = language if language else detected_language
        summary_data = await summarizer.generate_summary(transcript_text, metadata, language=summary_language)
        logger.info(f"✓ Summary generated")

        # Step N: Format markdown
        step_prefix = "Step 4/4" if use_youtube_captions else "Step 5/6"
        logger.info(f"{step_prefix}: Formatting markdown...")
        markdown_content = summarizer.format_markdown_note(summary_data, metadata)
        logger.info(f"✓ Markdown formatted ({len(markdown_content)} characters)")

        # Final step: Save to file if requested
        if save_to_file:
            logger.info("Saving to file...")

            # Resolve output directory path
            # If INVOCATION_DIR is set (by caller), use it as base for relative paths
            # Otherwise, use current working directory
            invocation_dir = os.environ.get('INVOCATION_DIR', os.getcwd())

            if output_path:
                output_path_obj = Path(output_path)
                if output_path_obj.is_absolute():
                    output_dir = output_path_obj
                else:
                    # Relative path: resolve against invocation directory
                    output_dir = Path(invocation_dir) / output_path
            else:
                # No output path specified, use settings default
                default_output = Path(settings.output_directory)
                if default_output.is_absolute():
                    output_dir = default_output
                else:
                    output_dir = Path(invocation_dir) / default_output

            # Create output directory only when saving to file
            if output_dir != Path('.') and not output_dir.exists():
                output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with date+refined_title format (YY_MM_DD-refined_title.md)
            import re
            from datetime import datetime

            # Get refined title from AI summary
            refined_title = summary_data.get('title', 'video_notes')
            if not refined_title or refined_title == 'video_notes':
                # Use video title as fallback and clean it
                refined_title = metadata.get('title', 'video_notes')

            # Clean refined title for cross-platform compatibility
            # Remove invalid filename characters (both ASCII and full-width variants)
            # Invalid: < > : " / \ | ? * （including full-width：）
            refined_title = re.sub(r'[<>:"/\\|?*\uff1a\u3001]', '_', refined_title)
            # Replace multiple spaces with single underscore
            refined_title = re.sub(r'\s+', '_', refined_title)
            # Remove leading/trailing spaces and dots
            refined_title = refined_title.strip('. ')
            # Limit refined title length (leave room for date prefix)
            if len(refined_title) > 100:
                refined_title = refined_title[:100]
            # Fallback if refined title becomes empty
            if not refined_title:
                refined_title = 'video_notes'

            # Generate date prefix in YY_MM_DD format
            date_prefix = datetime.now().strftime("%y_%m_%d")

            # Combine date and refined title
            filename = f"{date_prefix}-{refined_title}"

            output_file = output_dir / f"{filename}.md"

            # Write file with UTF-8 encoding
            output_file.write_text(markdown_content, encoding='utf-8')
            logger.info(f"✓ Saved to: {output_file}")
        else:
            logger.info("Skipping file save")

        return markdown_content

    finally:
        # Cleanup temporary files (but not local video files)
        logger.info("Cleaning up temporary files...")
        cleanup_video = video_path if video_path and not is_local_video else ""
        if cleanup_video or audio_path:
            video_processor.cleanup_temp_files(
                cleanup_video,
                audio_path if audio_path else ""
            )
        logger.info("✓ Cleanup completed")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Process video and generate AI-powered notes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process YouTube video
  python process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

  # Process Bilibili video with Chinese transcription
  python process_video.py --url "https://www.bilibili.com/video/BV1xx411c7XZ" --language zh

  # Process local video file (useful for Xiaohongshu videos downloaded manually)
  python process_video.py --local-video "./video.mp4" --video-title "My Video Title" --url "https://xiaohongshu.com/..."

  # Save to file
  python process_video.py --url "https://..." --save-to-file --output-path "./my_notes"

  # Use different AI model
  python process_video.py --url "https://..." --ai-model "google/gemini-2.5-flash"
        """
    )

    parser.add_argument(
        '--url',
        default='',
        help='Video URL (YouTube, Bilibili, or Xiaohongshu). Optional if --local-video is provided.'
    )

    parser.add_argument(
        '--local-video',
        help='Path to local video file (bypasses download, useful for manually downloaded videos)'
    )

    parser.add_argument(
        '--video-title',
        help='Video title (used with --local-video)'
    )

    parser.add_argument(
        '--language',
        help='Language code for transcription and summary (e.g., zh, en, ja, ko). If not specified, uses default from settings.'
    )

    parser.add_argument(
        '--ai-model',
        default=None,
        help='AI model to use for summarization (default: uses value from .env or anthropic/claude-3.5-sonnet)'
    )

    parser.add_argument(
        '--save-to-file',
        action='store_true',
        help='Save output to markdown file'
    )

    parser.add_argument(
        '--output-path',
        help='Output directory path (default: current directory)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--cookies',
        help='Path to cookies.txt file for YouTube authentication (bypass bot detection)'
    )

    parser.add_argument(
        '--use-youtube-captions',
        action='store_true',
        help='Use YouTube built-in captions instead of downloading video and using Whisper (faster, recommended for YouTube)'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate arguments
    if not args.url and not args.local_video:
        parser.error("Either --url or --local-video is required")

    try:
        # Run async processing
        markdown_output = asyncio.run(process_video(
            url=args.url,
            language=args.language,
            ai_model=args.ai_model,
            save_to_file=args.save_to_file,
            output_path=args.output_path,
            local_video=args.local_video,
            video_title=args.video_title,
            cookies_file=args.cookies,
            use_youtube_captions=args.use_youtube_captions
        ))

        # Output markdown to stdout (for skill consumption)
        print(markdown_output)

        sys.exit(0)

    except VideoDownloadError as e:
        logger.error(f"❌ Video download failed: {e}")
        sys.exit(1)

    except AudioExtractionError as e:
        logger.error(f"❌ Audio extraction failed: {e}")
        sys.exit(2)

    except TranscriptionError as e:
        logger.error(f"❌ Transcription failed: {e}")
        sys.exit(3)

    except SummarizationError as e:
        logger.error(f"❌ AI summarization failed: {e}")
        sys.exit(4)

    except ConfigurationError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(5)

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Process interrupted by user")
        sys.exit(130)

    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        sys.exit(99)


if __name__ == '__main__':
    main()
