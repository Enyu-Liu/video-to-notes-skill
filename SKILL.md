---
name: video-to-notes
description: Convert YouTube, Bilibili, and Xiaohongshu videos into AI-powered structured Markdown notes using local Whisper transcription. Use this skill when users want to: (1) Process video URLs from YouTube, Bilibili, or Xiaohongshu, (2) Generate learning notes or summaries from video content, (3) Extract and transcribe video audio offline, (4) Create study materials from video lectures or tutorials, (5) Process local video files. Keywords that trigger this skill include "video to notes", "summarize video", "transcribe video", "video summary", "YouTube notes", "Bilibili notes", "Xiaohongshu notes", "小红书", "video markdown".
---

# Video-to-Notes Skill

Convert YouTube, Bilibili, and Xiaohongshu videos into AI-powered structured Markdown notes using local OpenAI Whisper for transcription and OpenRouter for AI summarization.

## Quick Start

Process a video URL:

```bash
cd scripts
python process_video.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script will:
1. Download the video
2. Extract audio
3. Transcribe with local Whisper model
4. Generate AI summary with OpenRouter
5. Return formatted Markdown notes

## Prerequisites

The skill automatically checks for required dependencies when invoked. Ensure:

1. **System dependencies**:
   - FFmpeg (for audio extraction)
   - yt-dlp (for video downloads)
   - Python 3.10+ with pip

2. **API configuration** in `.env` file:
   - `OPENROUTER_API_KEY` - Required for AI summarization

3. **Python dependencies** (installed automatically):
   - `openai-whisper` for local transcription (no API key needed)
   - Other requirements from `requirements.txt`

## Core Workflow

When invoked, the skill:

1. **Validates environment**: Automatically checks FFmpeg, yt-dlp, and API key
2. **Processes video**: Calls `python scripts/process_video.py` with appropriate arguments
3. **Returns output**: Markdown notes to stdout (progress logs to stderr)
4. **Presents results**: Displays formatted Markdown to the user

### Command Structure

```bash
python scripts/process_video.py \
  --url "VIDEO_URL" \
  [--local-video PATH] \
  [--video-title TITLE] \
  [--language LANG_CODE] \
  [--ai-model MODEL_NAME] \
  [--cookies COOKIES_FILE] \
  [--save-to-file] \
  [--output-path PATH] \
  [--verbose]
```

### Required Arguments

- `--url`: Video URL (YouTube, Bilibili, or Xiaohongshu). Optional if `--local-video` is provided.

### Optional Arguments

- `--local-video`: Path to local video file (bypasses download, useful for manually downloaded videos)
- `--video-title`: Video title (used with `--local-video`)
- `--language`: Language code (e.g., 'zh', 'en'). Omit for auto-detection.
- `--ai-model`: AI model for summarization (default: anthropic/claude-3.5-sonnet)
- `--cookies`: Path to cookies.txt file for YouTube authentication (bypass bot detection)
- `--use-youtube-captions`: **Recommended for YouTube** - Use YouTube's built-in captions instead of downloading video (faster, bypasses download restrictions)
- `--save-to-file`: Save output to markdown file in addition to stdout
- `--output-path`: Custom output directory (default: current directory)
- `--verbose`: Enable debug logging

## Common Usage Patterns

### YouTube video with captions (Recommended - Fast, No Download)
```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --use-youtube-captions --save-to-file
```

This method:
- Uses YouTube's built-in captions (no video download needed)
- Bypasses YouTube bot detection and 403 errors
- Much faster (~10 seconds vs ~60+ seconds)
- Works without cookies

### Basic video processing (with download)
```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Chinese video with language hint
```bash
python scripts/process_video.py \
  --url "https://www.bilibili.com/video/BV1xx411c7XZ" \
  --language zh
```

### Xiaohongshu video (within mainland China)
```bash
python scripts/process_video.py \
  --url "https://www.xiaohongshu.com/explore/VIDEO_ID" \
  --language zh
```

### Local video file (for manually downloaded videos)
```bash
python scripts/process_video.py \
  --local-video "./downloaded_video.mp4" \
  --video-title "Video Title" \
  --url "https://original-source-url" \
  --language zh
```

### Save to file
```bash
python scripts/process_video.py \
  --url "https://..." \
  --save-to-file \
  --output-path "./my_notes"
```

### Use different AI model
```bash
python scripts/process_video.py \
  --url "https://..." \
  --ai-model "google/gemini-2.5-flash"
```

## Output Format

The script generates structured Markdown with the following features:

**Format Enhancements:**
- **Code formatting**: Technical terms, commands, and function names use `inline code` format
- **Multi-line code blocks**: Code snippets use proper ``` syntax with language identifiers
- **Smart examples**: When concepts are complex or abstract, the AI provides concrete examples that:
  - Are closely tied to the video content
  - Are naturally integrated into the note structure
  - Help clarify technical details or abstract ideas
  - Avoid over-expansion while maintaining clarity

**Example structure:**

```markdown
# Refined Title Based on Video Content

**来源**: [Video URL]
**时长**: HH:MM:SS
**作者**: Channel Name
**处理时间**: YYYY-MM-DD HH:MM:SS

> **核心要点**
> 1. First key point
> 2. Second key point
> 3. Third key point

## 1. Section Title

Detailed content with proper formatting. Technical terms like `React` and `HTTP` are
formatted as inline code. When discussing implementation:

```python
# Example code with syntax highlighting
def example_function():
    return "Hello World"
```

The video explains this concept using a practical example: imagine a scenario where...

### 1.1 Subsection Title

More detailed content naturally integrating examples when needed...

## 2. Next Section Title

...
```

## Performance

**Typical processing time for 8-minute video (with `base` Whisper model):**
- Video download: ~7 seconds
- Audio extraction: ~1 second
- Local Whisper transcription: ~30-60 seconds (CPU) or ~10-20 seconds (GPU)
- AI summarization: ~5-6 seconds
- **Total: ~50-80 seconds (CPU) or ~25-35 seconds (GPU)**

**Note**: First run downloads the Whisper model (~150MB for `base` model).

## Error Handling

The script uses exit codes to indicate errors:

- `0`: Success
- `1`: Video download error
- `2`: Audio extraction error
- `3`: Transcription error
- `4`: Summarization error
- `5`: Configuration error
- `130`: User interrupted (Ctrl+C)
- `99`: Unexpected error

When errors occur, check:

1. **Network connection**: Required for video download and OpenRouter API
2. **API key**: Ensure OPENROUTER_API_KEY is valid
3. **FFmpeg**: Verify with `ffmpeg -version`
4. **yt-dlp**: Verify with `yt-dlp --version`
5. **Video accessibility**: Check if video is public and not region-blocked
6. **Hardware**: Ensure sufficient RAM/VRAM for Whisper model

## Limitations

1. **Video length**: Can process long videos (no audio file size limit like API-based solutions)
2. **Platforms**: Supports YouTube, Bilibili, and Xiaohongshu
3. **YouTube bot detection**: YouTube may require authentication. Use `--cookies` option with exported cookies file.
4. **Xiaohongshu regional restriction**: Xiaohongshu blocks access from outside mainland China. Use `--local-video` option for manually downloaded videos.
5. **API costs**: Only AI summarization costs (~$0.02-0.05 per video). Transcription is FREE.
6. **Processing location**: Script runs locally; requires internet for download and AI API only
7. **Hardware**: Larger Whisper models require more RAM/VRAM

## YouTube Bot Detection Bypass

YouTube has strengthened its anti-bot measures. If you encounter "Sign in to confirm you're not a bot" errors, use cookies authentication:

### Step 1: Export YouTube Cookies

Use a browser extension to export cookies in Netscape format:

**Recommended extensions:**
- **Chrome**: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) or [Export Cookies](https://chromewebstore.google.com/detail/export-cookies/okchdmicnlfpkoikbkllnmjmkjhldehe)
- **Firefox**: [cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)
- **Edge**: Search for "cookies.txt" in Edge Add-ons

**Export steps:**
1. Install a cookies export extension
2. Log in to YouTube in your browser
3. Navigate to youtube.com
4. Click the extension icon and export cookies
5. Save as `cookies.txt` in the scripts directory

### Step 2: Use Cookies with the Script

```bash
python scripts/process_video.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies "./cookies.txt" \
  --save-to-file
```

### Environment Variable (Optional)

You can set a default cookies file in `.env`:

```env
YOUTUBE_COOKIES=./cookies.txt
```

### Important Notes

- **Keep cookies private**: Never share your cookies.txt file
- **Refresh periodically**: Cookies may expire; re-export if downloads fail
- **Close browser first**: Some browsers lock cookies; close Chrome/Edge before exporting
- **Alternative**: Use `--local-video` option with manually downloaded videos

## Xiaohongshu Support

Xiaohongshu (小红书) videos have regional restrictions. If you're accessing from outside mainland China:

1. **Download manually**: Use tools like [dlbunny.com/en/xhs](https://dlbunny.com/en/xhs) to download the video
2. **Use local-video option**: Process the downloaded video with:
   ```bash
   python scripts/process_video.py \
     --local-video "./xiaohongshu_video.mp4" \
     --video-title "视频标题" \
     --url "https://www.xiaohongshu.com/explore/VIDEO_ID" \
     --language zh \
     --save-to-file
   ```

## Advanced Configuration

### Environment Variables

Create `.env` file in scripts directory:

```env
# Required
OPENROUTER_API_KEY=sk-or-v1-...

# Whisper model size (tiny/base/small/medium/large)
WHISPER_MODEL=base

# Default language (zh/en/auto)
DEFAULT_LANGUAGE=zh

# Optional
AI_MODEL=google/gemini-2.5-flash
OUTPUT_DIRECTORY=.
TEMP_DIRECTORY=./temp
LOG_LEVEL=INFO
MAX_VIDEO_LENGTH=7200
```

### Whisper Model Selection

| Model | VRAM | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `tiny` | ~1GB | Fastest | Basic | Quick drafts |
| `base` | ~1GB | Fast | Good | **Default** |
| `small` | ~2GB | Medium | Better | Better accuracy |
| `medium` | ~5GB | Slow | High | Quality work |
| `large` | ~10GB | Slowest | Best | Professional |

### Recommended AI Models

**For summarization (OpenRouter):**
- `google/gemini-2.5-flash` - Fast, cheap, good quality (**Recommended**)
- `anthropic/claude-3.5-sonnet` - Best quality, moderate cost
- `openai/gpt-4-turbo` - High quality, higher cost

## Troubleshooting

**Quick fixes:**

- **"OpenRouter API key required"**: Set OPENROUTER_API_KEY in `.env`
- **"FFmpeg failed"**: Install FFmpeg or check PATH
- **"Failed to load Whisper model"**: Insufficient RAM/VRAM or network issue on first download
- **"Video too long"**: Exceeds MAX_VIDEO_LENGTH (default 2 hours)
- **Slow transcription**: Use smaller Whisper model (e.g., `WHISPER_MODEL=tiny`)

## Implementation Notes

When implementing this skill:

1. **Check prerequisites first**: Before calling the script, verify FFmpeg, yt-dlp, and OpenRouter API key
2. **Set working directory**: Always `cd scripts/` before running the script
3. **Capture stdout/stderr separately**: Output goes to stdout, logs to stderr
4. **Handle long processing times**: Video processing can take 30-90 seconds (longer for CPU transcription)
5. **Inform user of progress**: The script logs progress to stderr
6. **Parse exit codes**: Use exit codes to provide specific error messages
7. **First run delay**: Whisper model downloads on first use (~150MB-3GB depending on model)

## Advantages of Local Whisper

✅ **No transcription API costs** - Only pay for AI summarization
✅ **No file size limits** - Process videos of any length
✅ **Works offline** - Transcription works without internet (after model download)
✅ **Privacy** - Audio never leaves your machine
✅ **Unlimited usage** - No API rate limits

## Architecture

```
video-to-notes-skill/
├── SKILL.md                   # This file (Claude Code skill definition)
├── LICENSE                    # MIT License
├── README.md                  # English documentation
├── README_zh.md               # Chinese documentation
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── scripts/                   # Core processing scripts
    ├── process_video.py       # Main CLI script
    ├── requirements.txt       # Python dependencies
    ├── pyproject.toml         # Python project config
    ├── core/                  # Core modules
    │   ├── video_processor.py # yt-dlp + FFmpeg
    │   ├── youtube_transcript.py  # YouTube captions
    │   ├── xiaohongshu_downloader.py  # Xiaohongshu support
    │   ├── transcriber.py     # Local Whisper model
    │   ├── summarizer.py      # OpenRouter API
    │   └── exceptions.py      # Custom exceptions
    └── config/
        └── settings.py        # Configuration management
```
