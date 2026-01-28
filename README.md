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
- 📝 **Format-aware**: Auto-formats code with Markdown (`inline code`, ```code blocks```)
- 💡 **Smart expansion**: Provides clear examples for complex concepts, naturally integrated into notes

## 🚀 Quick Start

> **Note for Claude Code Users**: When using this skill in Claude Code, the environment will be checked automatically. You only need to ensure FFmpeg, yt-dlp, and Python dependencies are installed, and your OpenRouter API key is configured.

### Manual Setup (for standalone use)

#### 1. Install System Dependencies

- **FFmpeg** (for audio extraction): [Download FFmpeg](https://ffmpeg.org/download.html)
- **yt-dlp** (for video downloading): `pip install yt-dlp`

#### 2. Setup Python Environment

```bash
cd scripts

# Install Python dependencies
pip install -r requirements.txt
# Or use uv for faster installation:
# uv pip install -r requirements.txt
```

#### 3. Configure Environment

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
DEFAULT_LANGUAGE=zh
OUTPUT_DIRECTORY=.
TEMP_DIRECTORY=./temp
LOG_LEVEL=INFO
MAX_VIDEO_LENGTH=7200
```

**Language Configuration:**
- `DEFAULT_LANGUAGE`: Set your preferred language for transcription and AI summary
  - `zh` - Chinese (中文) - **Default**
  - `en` - English
  - `auto` - Auto-detect

**Note:** The language setting affects both Whisper transcription and AI-generated summary output.

**Get API Key**: Visit [OpenRouter.ai](https://openrouter.ai/), sign up, create API key, add credits ($5-10 is enough for hundreds of videos).

## 💻 Usage

### Claude Code Integration

Use natural language to interact with the skill in Claude Code:

**Basic Usage:**
```
Please convert this YouTube video to notes: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```
请将这个Bilibili视频转换为中文笔记：https://www.bilibili.com/video/BV1LzqLBaE1B
```

**With Specific Language:**
```
Summarize this video in English: https://www.youtube.com/watch?v=VIDEO_ID
```

```
Summarize this video in Chinese: https://www.bilibili.com/video/BV...
```

**Save to File:**
```
Please process this video and save the notes to ./notes directory: https://...
```

```
请处理这个视频并将笔记保存到 my_notes 文件夹：https://...
```

**Advanced Options:**
```
Convert this video to notes using Claude for summarization: https://...
```

```
请用 Gemini AI 模型处理这个视频并生成笔记：https://...
```

**Multiple Language Support:**
- Chinese: "请将这个视频转换为中文笔记"
- English: "Convert this video to English notes"
- Auto-detect: "Convert this video to notes" (language will be auto-detected)


## ⚙️ Parameters

| Parameter | Type | Required | Description | Examples |
|-----------|------|----------|-------------|----------|
| `url` | string | ✅ Yes | Video URL (YouTube or Bilibili) | `https://www.youtube.com/watch?v=...`<br>`https://www.bilibili.com/video/BV...` |
| `--language` | string | No | Language code for transcription | `zh` (Chinese)<br>`en` (English)<br>`auto` (auto-detect) |
| `--ai-model` | string | No | AI model for summarization | `google/gemini-2.5-flash` (recommended)<br>`anthropic/claude-3.5-sonnet`<br>`openai/gpt-4-turbo` |
| `--save-to-file` | flag | No | Save output to markdown file | `--save-to-file` |
| `--output-path` | string | No | Output directory path | `./my_notes`<br>`../notes`<br>`/path/to/notes` |
| `--verbose` | flag | No | Enable verbose logging | `--verbose` |

### Language Options

| Code | Language | Example Usage |
|------|----------|---------------|
| `auto` | Auto-detect (default) | `--language auto` |
| `zh` | Chinese (中文) | `--language zh` |
| `en` | English | `--language en` |

### AI Model Options

| Model | Provider | Speed | Cost | Quality | Use Case |
|-------|----------|-------|------|---------|----------|
| `google/gemini-2.5-flash` | Google | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | **Recommended** - Fast, affordable |
| `anthropic/claude-3.5-sonnet` | Anthropic | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best quality, detailed analysis |
| `openai/gpt-4-turbo` | OpenAI | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | High quality, balanced |

### Output Path Options

| Path Type | Example | Description |
|-----------|---------|-------------|
| Current | `.` | Current directory (default) |
| Relative | `./notes` | Subdirectory relative to current location |
| Relative | `../my_notes` | Parent directory |
| Absolute | `/Users/name/Desktop/notes` | Full system path |

## 📊 Output Example

Generated notes have the following format features:

**Format Enhancements:**
- **Code formatting**: Technical terms, commands, function names use `inline code` format
- **Multi-line code blocks**: Code snippets use proper ``` syntax with language identifiers
- **Smart examples**: When concepts are complex or abstract, AI provides concrete examples that:
  - Are closely tied to video content
  - Are naturally integrated into note structure
  - Help clarify technical details or abstract concepts
  - Avoid over-expansion while maintaining clarity

**Example structure:**

```markdown
# Refined Title Based on Video Content

**Source**: https://www.youtube.com/watch?v=...
**Duration**: 0:08:45
**Author**: Channel Name
**Processed**: 2025-01-15 14:30:00

> **Core Points**
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

More detailed content, naturally integrating examples when needed...

## 2. Next Section Title

...
```

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | ✅ Yes | - | OpenRouter API key for AI summarization |
| `AI_MODEL` | No | `anthropic/claude-3.5-sonnet` | AI model for summarization |
| `WHISPER_MODEL` | No | `base` | Whisper model size (tiny/base/small/medium/large) |
| `DEFAULT_LANGUAGE` | No | `zh` | Default language for transcription and summary (zh/en/auto) |
| `OUTPUT_DIRECTORY` | No | `.` | Output directory for saved notes (default: current directory) |
| `TEMP_DIRECTORY` | No | `./temp` | Temporary directory (always in skill folder, auto-created) |
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
