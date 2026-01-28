# Video-to-Notes Skill

Convert YouTube/Bilibili videos into AI-powered Markdown notes.

Local Whisper transcription (free) + OpenRouter API summarization (~$0.02/video)

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[中文文档](README_zh.md)

## Features

- **Cost-effective**: Free local transcription, only pay for AI summary
- **Privacy-focused**: Audio processed locally
- **Multi-platform**: YouTube, Bilibili, Xiaohongshu

## Quick Start

### 1. Install Dependencies

```bash
# System dependencies
# - FFmpeg: https://ffmpeg.org/download.html
# - yt-dlp: pip install yt-dlp

# Python dependencies
cd scripts
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env, add your OpenRouter API key
```

Get API key from [OpenRouter.ai](https://openrouter.ai/)

### 3. Run

```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --language zh --save-to-file
```

## Usage

### In Claude Code

```
Please convert this video to notes: https://www.youtube.com/watch?v=...
```

```
请将这个视频转换为中文笔记：https://www.bilibili.com/video/BV...
```

### Command Line

```bash
# Basic
python scripts/process_video.py --url "VIDEO_URL"

# With options
python scripts/process_video.py \
  --url "VIDEO_URL" \
  --language zh \
  --save-to-file \
  --output-path "./notes"
```

**Parameters:**
- `--url` - Video URL (required)
- `--language` - Language code: `zh`, `en`, `auto`
- `--ai-model` - AI model (default: `google/gemini-2.5-flash`)
- `--save-to-file` - Save to markdown file
- `--output-path` - Output directory

## Output Example

See [examples/github-spec-kit-notes.md](examples/github-spec-kit-notes.md) for a real output.

**Format features:**
- Structured sections with core points summary
- Code formatting with syntax highlighting
- Smart examples for complex concepts

## Configuration

**`.env` file:**

```env
OPENROUTER_API_KEY=sk-or-your-key-here  # Required
AI_MODEL=google/gemini-2.5-flash        # Optional
WHISPER_MODEL=base                       # Optional: tiny/base/small/medium/large
DEFAULT_LANGUAGE=zh                      # Optional: zh/en/auto
```

## Architecture

```
Video URL → yt-dlp → FFmpeg → Whisper (local) → OpenRouter API → Markdown
```

## License

MIT License - See [LICENSE](LICENSE)
