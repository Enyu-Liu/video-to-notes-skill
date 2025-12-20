"""Main script for processing videos and generating notes

This script can be used standalone or called by Claude Skills.
"""

import asyncio
import sys
import argparse
import logging
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
    output_path: Optional[str] = None
) -> str:
    """
    Process video and return markdown notes

    Args:
        url: Video URL (YouTube or Bilibili)
        language: Optional language code for transcription
        ai_model: Optional AI model override
        save_to_file: Whether to save output to file
        output_path: Optional output directory path

    Returns:
        Markdown formatted notes

    Raises:
        Various exceptions if processing fails
    """
    settings = get_settings()
    video_processor = VideoProcessor()

    # Initialize components
    try:
        from core.transcriber import Transcriber
        transcriber = Transcriber()
        logger.info(f"Using local Whisper model: {settings.whisper_model}")

        summarizer = Summarizer(model=ai_model)
    except Exception as e:
        raise ConfigurationError(f"Failed to initialize components: {str(e)}")

    video_path = None
    audio_path = None

    try:
        # Step 1: Download video
        logger.info(f"Step 1/6: Downloading video from {url}")
        video_path, metadata = video_processor.download_video(url)
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

        # Step 4: Generate AI summary
        logger.info("Step 4/6: Generating AI summary...")
        summary_data = await summarizer.generate_summary(transcript_text, metadata)
        logger.info(f"✓ Summary generated")

        # Step 5: Format markdown
        logger.info("Step 5/6: Formatting markdown...")
        markdown_content = summarizer.format_markdown_note(summary_data, metadata)
        logger.info(f"✓ Markdown formatted ({len(markdown_content)} characters)")

        # Step 6: Save to file if requested
        if save_to_file:
            logger.info("Step 6/6: Saving to file...")
            output_dir = Path(output_path if output_path else settings.output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename from summary title
            filename = summary_data.get('title', 'video_notes').replace(' ', '_')
            # Clean filename
            import re
            filename = re.sub(r'[^\w\s-]', '', filename)
            filename = re.sub(r'\s+', '_', filename)
            output_file = output_dir / f"{filename}.md"

            # Write file
            output_file.write_text(markdown_content, encoding='utf-8')
            logger.info(f"✓ Saved to: {output_file}")
        else:
            logger.info("Step 6/6: Skipping file save")

        return markdown_content

    finally:
        # Cleanup temporary files
        logger.info("Cleaning up temporary files...")
        if video_path or audio_path:
            video_processor.cleanup_temp_files(
                video_path if video_path else "",
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

  # Save to file
  python process_video.py --url "https://..." --save-to-file --output-path "./my_notes"

  # Use different AI model
  python process_video.py --url "https://..." --ai-model "google/gemini-2.5-flash"
        """
    )

    parser.add_argument(
        '--url',
        required=True,
        help='Video URL (YouTube or Bilibili)'
    )

    parser.add_argument(
        '--language',
        help='Language code for transcription (e.g., zh, en). If not specified, auto-detects.'
    )

    parser.add_argument(
        '--ai-model',
        default='anthropic/claude-3.5-sonnet',
        help='AI model to use for summarization (default: anthropic/claude-3.5-sonnet)'
    )

    parser.add_argument(
        '--save-to-file',
        action='store_true',
        help='Save output to markdown file'
    )

    parser.add_argument(
        '--output-path',
        help='Output directory path (default: ./notes)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Run async processing
        markdown_output = asyncio.run(process_video(
            url=args.url,
            language=args.language,
            ai_model=args.ai_model,
            save_to_file=args.save_to_file,
            output_path=args.output_path
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
