# 🎬 Video-to-Notes Skill

> Transform any YouTube/Bilibili video into structured AI-powered notes — just by chatting with Claude.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[中文文档](README_zh.md)

---

## ✨ What This Does

Drop a video URL in Claude Code, and get back:
- **Structured markdown notes** with key points, chapters, and code examples
- **Smart formatting** for technical content (commands, code blocks, examples)
- **Privacy-first processing** - audio never leaves your machine
- **Ultra-low cost** - ~$0.02 per video (only AI summary costs money)

**Perfect for:** Tutorial videos, tech talks, lectures, documentation videos

---

## 🚀 Quick Setup

### Step 1: Install Dependencies

**System Requirements:**
- [FFmpeg](https://ffmpeg.org/download.html) - for audio extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - `pip install yt-dlp`

**Python Dependencies:**
```bash
cd scripts
pip install -r requirements.txt
```

### Step 2: Get Your API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up and create an API key
3. Add $5-10 credits (enough for 200+ videos)

### Step 3: Configure

```bash
cp .env.example .env
# Edit .env and add: OPENROUTER_API_KEY=sk-or-your-key-here
```

**That's it!** The skill is ready to use.

---

## 💬 How to Use

### In Claude Code (Recommended)

Just talk naturally to Claude:

**English:**
```
Convert this video to notes: https://www.youtube.com/watch?v=a9eR1xsfvHg
```

```
Summarize this tutorial in English: https://www.youtube.com/watch?v=...
```

```
Please save the notes to my Desktop/notes folder
```

**中文:**
```
请将这个视频转换为笔记：https://www.bilibili.com/video/BV1xx411c7XZ
```

```
帮我总结这个教程，用中文
```

```
把笔记保存到我的文档文件夹
```

**Claude will:**
1. ✅ Check your environment automatically
2. ✅ Download and process the video
3. ✅ Generate beautiful markdown notes
4. ✅ Save to file if you ask

---

## 📊 What You Get

See real example: [examples/github-spec-kit-notes.md](examples/github-spec-kit-notes.md)

**Every note includes:**
- Clear title based on video content
- Video metadata (source, duration, author, timestamp)
- Core takeaways summary (3-7 bullet points)
- Structured sections with hierarchical headings
- Technical terms formatted as `inline code`
- Code examples with syntax highlighting
- Smart examples when concepts are complex

---

## 🎯 Capabilities

| Feature | Details |
|---------|---------|
| **Platforms** | YouTube, Bilibili, Xiaohongshu |
| **Languages** | Auto-detect, or specify: Chinese, English, Japanese, etc. |
| **Video Length** | Up to 2 hours (configurable) |
| **Speed** | ~2-3 minutes for an 8-minute video |
| **Cost** | ~$0.02-0.05 per video (AI summary only) |
| **Privacy** | Audio processed locally with Whisper |

**AI Models Available:**
- `google/gemini-2.5-flash` (default - fast & cheap)
- `anthropic/claude-3.5-sonnet` (best quality)
- `openai/gpt-4-turbo` (balanced)

---

## ⚙️ Advanced Configuration

### Environment Variables (Optional)

Edit `.env` to customize:

```env
# Required
OPENROUTER_API_KEY=sk-or-your-key-here

# Optional - customize these if needed
AI_MODEL=google/gemini-2.5-flash    # Which AI to use
WHISPER_MODEL=base                   # Whisper model: tiny/base/small/medium/large
DEFAULT_LANGUAGE=zh                  # Default language: zh/en/auto
OUTPUT_DIRECTORY=.                   # Where to save notes
```

### Whisper Models

| Model | Speed | Accuracy | RAM | Best For |
|-------|-------|----------|-----|----------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | 1GB | Quick drafts |
| `base` | ⚡⚡ | ⭐⭐⭐ | 1GB | **Default** - balanced |
| `small` | ⚡ | ⭐⭐⭐⭐ | 2GB | Better accuracy |
| `medium` | 🐌 | ⭐⭐⭐⭐⭐ | 5GB | High quality |

---

## 🛠️ For Developers

### Architecture

```
Video URL → yt-dlp → FFmpeg → Whisper (local) → OpenRouter API → Markdown
```

### Command Line Usage

If you prefer running scripts directly:

```bash
python scripts/process_video.py \
  --url "https://www.youtube.com/watch?v=..." \
  --language zh \
  --save-to-file \
  --output-path "./notes"
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

<div align="center">

**Built with** [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [FFmpeg](https://ffmpeg.org/) · [OpenAI Whisper](https://github.com/openai/whisper) · [OpenRouter](https://openrouter.ai/)

⭐ Star this repo if it helps you!

</div>
