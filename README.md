# Video-to-Notes Skill

<div align="center">

🚀 **Convert YouTube and Bilibili videos into AI-powered Markdown notes**

Local Whisper transcription + OpenRouter API summarization

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

🌐 **Other Languages**: [中文](README_zh.md)

</div>

---

## What is Video-to-Notes?

Convert YouTube and Bilibili videos into structured AI-powered Markdown notes using local Whisper transcription (free) + OpenRouter API for summarization.

**Why use this?**
- 💰 **Cost-effective**: Free local transcription, only pay for AI summary (~$0.02-0.05 per video)
- 🔒 **Privacy-focused**: Audio processed locally, never leaves your machine
- 🌍 **Multi-platform**: YouTube, Bilibili
- ⚡ **Fast**: 2-3 minutes for an 8-minute video

## 🚀 Quick Start

### 1. Install System Dependencies

**FFmpeg** (Required for audio extraction):
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

**yt-dlp** (Required for video downloading):
```bash
# Install globally as a system tool
pip install yt-dlp
```

### 2. Setup Python Environment (with uv)

```bash
# Clone the repository
git clone https://github.com/Enyu-Liu/video-to-notes-skill.git
cd video-to-notes-skill/scripts

# Create virtual environment with uv (recommended)
uv venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
uv pip install -r requirements.txt
```

**Note**: `yt-dlp` appears in both system installation (for CLI) and `requirements.txt` (for Python import). Both are required.

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenRouter API key
```

**`.env` Configuration**:
```env
# Required: OpenRouter API Key (get from https://openrouter.ai/)
OPENROUTER_API_KEY=sk-or-your-key-here

# Optional configurations
AI_MODEL=google/gemini-2.5-flash
WHISPER_MODEL=base
OUTPUT_DIRECTORY=./notes
TEMP_DIRECTORY=./temp
LOG_LEVEL=INFO
MAX_VIDEO_LENGTH=7200
```

**Get API Key**: Visit [OpenRouter.ai](https://openrouter.ai/), sign up, create API key, add credits ($5-10 is enough for hundreds of videos).

## 💻 Usage

### Claude Code Integration

Use the skill directly in Claude Code:

```
/video-to-notes https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```
/video-to-notes https://www.bilibili.com/video/BV1LzqLBaE1B --language zh
```

```
/video-to-notes https://... --save-to-file --output-path ./notes
```

## ⚙️ Parameters

| Parameter | Type | Required | Description | Examples |
|-----------|------|----------|-------------|----------|
| `url` | string | ✅ Yes | Video URL (YouTube or Bilibili) | `https://www.youtube.com/watch?v=...`<br>`https://www.bilibili.com/video/BV...` |
| `--language` | string | No | Language code for transcription | `zh` (Chinese)<br>`en` (English)<br>`ja` (Japanese)<br>`ko` (Korean)<br>`auto` (auto-detect) |
| `--ai-model` | string | No | AI model for summarization | `google/gemini-2.5-flash` (recommended)<br>`anthropic/claude-3.5-sonnet`<br>`openai/gpt-4-turbo` |
| `--save-to-file` | flag | No | Save output to markdown file | `--save-to-file` |
| `--output-path` | string | No | Outputmy_notes`<br>` directory path | `.//path/to/notes` |
| `--verbose` | flag | No | Enable verbose logging | `--verbose` |

### Language Options

| Code | Language | Example Usage |
|------|----------|---------------|
| `auto` | Auto-detect (default) | `--language auto` |
| `zh` | Chinese (中文) | `--language zh` |
| `en` | English | `--language en` |
| `ja` | Japanese (日本語) | `--language ja` |
| `ko` | Korean (한국어) | `--language ko` |
| `es` | Spanish (Español) | `--language es` |
| `fr` | French (Français) | `--language fr` |
| `de` | German (Deutsch) | `--language de` |

### AI Model Options

| Model | Provider | Speed | Cost | Quality | Use Case |
|-------|----------|-------|------|---------|----------|
| `google/gemini-2.5-flash` | Google | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | **Recommended** - Fast, affordable |
| `anthropic/claude-3.5-sonnet` | Anthropic | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best quality, detailed analysis |
| `openai/gpt-4-turbo` | OpenAI | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | High quality, balanced |

### Output Path Options

| Path Type | Example | Description |
|-----------|---------|-------------|
| Relative | `./notes` | Relative to `scripts/` directory |
| Relative | `../my_notes` | Parent directory |
| Absolute | `/Users/name/Desktop/notes` | Full system path |
| Custom | `./output/video_notes` | Custom subdirectory |

## 📊 Output Example

```markdown
# Video Title

## Core Points
- Key point 1
- Key point 2
- Key point 3

## Detailed Summary
AI-generated detailed summary of the video content...

---
**Source**: https://www.youtube.com/watch?v=...
**Duration**: 0:08:45
**Author**: Channel Name
**Processed**: 2025-01-15 14:30:00
```

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | ✅ Yes | - | OpenRouter API key for AI summarization |
| `AI_MODEL` | No | `anthropic/claude-3.5-sonnet` | AI model for summarization |
| `WHISPER_MODEL` | No | `base` | Whisper model size (tiny/base/small/medium/large) |
| `OUTPUT_DIRECTORY` | No | `./notes` | Output directory for saved notes |
| `TEMP_DIRECTORY` | No | `./temp` | Temporary directory for processing |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_VIDEO_LENGTH` | No | `7200` | Maximum video length in seconds (2 hours) |

### Whisper Models

| Model | Size | RAM/VRAM | Speed | Accuracy | Recommended For |
|-------|------|----------|-------|----------|----------------|
| `tiny` | ~39 MB | ~1 GB | Fastest | Basic | Quick drafts, low-end hardware |
| `base` | ~74 MB | ~1 GB | Fast | Good | **Default** - balanced performance |
| `small` | ~244 MB | ~2 GB | Medium | Better | General use with decent GPU |
| `medium` | ~769 MB | ~5 GB | Slow | High | Quality-focused workflows |
| `large` | ~1550 MB | ~10 GB | Slowest | Best | Professional transcription |

## ⚡ Performance

**Processing time (8-minute video, base model)**:
- Video download: ~7 seconds
- Audio extraction: ~1 second
- Local Whisper transcription: ~30-60 seconds (CPU) or ~10-20 seconds (GPU)
- AI summarization: ~5-6 seconds
- **Total: ~50-80 seconds (CPU) or ~25-35 seconds (GPU)**

**First run**: Downloads Whisper model (~150MB for base model)

## 💰 Cost

**Per 8-minute video**:
- Local Whisper transcription: **FREE** (uses your hardware)
- OpenRouter (Gemini 2.5 Flash): ~$0.02-0.05
- **Total: ~$0.02-0.05 per video**

## 🛠️ Architecture

- **Video Download**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Audio Extraction**: [FFmpeg](https://ffmpeg.org/)
- **Speech-to-Text**: [OpenAI Whisper](https://github.com/openai/whisper) (local)
- **AI Summarization**: [OpenRouter](https://openrouter.ai/) (Claude/Gemini etc)
- **Environment Management**: [uv](https://github.com/astral-sh/uv) (recommended)

## 📜 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download
- [FFmpeg](https://ffmpeg.org/) - Audio extraction
- [OpenAI Whisper](https://github.com/openai/whisper) - Local transcription
- [OpenRouter](https://openrouter.ai/) - AI summarization

---

<div align="center">

⭐ **Star this repo if helpful!**

[⬆ Back to Top](#video-to-notes-skill)

</div>
