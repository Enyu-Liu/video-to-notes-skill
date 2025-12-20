---
name: video-to-notes
description: Convert YouTube and Bilibili videos into AI-powered structured Markdown notes using local Whisper transcription. Use this skill when users want to: (1) Process video URLs from YouTube or Bilibili, (2) Generate learning notes or summaries from video content, (3) Extract and transcribe video audio offline, (4) Create study materials from video lectures or tutorials. Keywords that trigger this skill include "video to notes", "summarize video", "transcribe video", "video summary", "YouTube notes", "Bilibili notes", "video markdown".
---

# Video-to-Notes Skill

Convert YouTube and Bilibili videos into AI-powered structured Markdown notes using local OpenAI Whisper for transcription and OpenRouter for AI summarization.

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

Before using this skill, ensure:

1. **System dependencies are installed**:
   - FFmpeg (for audio extraction)
   - yt-dlp (for video downloads)
   - Python 3.10+ with pip

2. **API keys are configured** in `.env` file:
   - `OPENROUTER_API_KEY` - For AI summarization

3. **Python dependencies are installed**:
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

   This installs `openai-whisper` for local transcription (no API key needed).

## Core Workflow

When a user requests video processing:

1. **Validate environment**: Check that FFmpeg and yt-dlp are available
2. **Check API key**: Verify OPENROUTER_API_KEY is set
3. **Call the script**: Execute `python scripts/process_video.py` with appropriate arguments
4. **Parse output**: The script outputs Markdown to stdout (progress logs go to stderr)
5. **Present results**: Show the formatted Markdown notes to the user

### Command Structure

```bash
python scripts/process_video.py \
  --url "VIDEO_URL" \
  [--language LANG_CODE] \
  [--ai-model MODEL_NAME] \
  [--save-to-file] \
  [--output-path PATH] \
  [--verbose]
```

### Required Arguments

- `--url`: Video URL (YouTube or Bilibili)

### Optional Arguments

- `--language`: Language code (e.g., 'zh', 'en'). Omit for auto-detection.
- `--ai-model`: AI model for summarization (default: anthropic/claude-3.5-sonnet)
- `--save-to-file`: Save output to markdown file in addition to stdout
- `--output-path`: Custom output directory (default: ./notes)
- `--verbose`: Enable debug logging

## Common Usage Patterns

### Basic video processing
```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Chinese video with language hint
```bash
python scripts/process_video.py \
  --url "https://www.bilibili.com/video/BV1xx411c7XZ" \
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

The script generates structured Markdown:

```markdown
# Video Title

## 核心要点
- Key point 1
- Key point 2
- Key point 3

## 详细总结
Detailed AI-generated summary...

---
**来源**: [Video URL]
**时长**: HH:MM:SS
**作者**: Channel Name
**处理时间**: YYYY-MM-DD HH:MM:SS
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
2. **Platforms**: Currently supports YouTube and Bilibili only
3. **API costs**: Only AI summarization costs (~$0.02-0.05 per video). Transcription is FREE.
4. **Processing location**: Script runs locally; requires internet for download and AI API only
5. **Hardware**: Larger Whisper models require more RAM/VRAM

## Advanced Configuration

### Environment Variables

Create `.env` file in scripts directory:

```env
# Required
OPENROUTER_API_KEY=sk-or-v1-...

# Whisper model size (tiny/base/small/medium/large)
WHISPER_MODEL=base

# Optional
AI_MODEL=google/gemini-2.5-flash
OUTPUT_DIRECTORY=./notes
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

For detailed troubleshooting information, see [references/troubleshooting.md](references/troubleshooting.md).

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
├── SKILL.md                   # This file
├── scripts/                   # Core processing scripts
│   ├── process_video.py       # Main CLI script
│   ├── core/                  # Core modules
│   │   ├── video_processor.py # yt-dlp + FFmpeg
│   │   ├── transcriber.py     # Local Whisper model
│   │   ├── summarizer.py      # OpenRouter API
│   │   └── exceptions.py      # Custom exceptions
│   ├── config/
│   │   └── settings.py        # Configuration management
│   └── requirements.txt       # Python dependencies
├── .env.example               # Environment template
├── .env                       # Your configuration (git-ignored)
├── references/
│   └── troubleshooting.md     # Detailed troubleshooting
└── README.md                  # User documentation
```
