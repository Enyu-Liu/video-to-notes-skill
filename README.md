# Video-to-Notes Skill | 视频转笔记技能

<div align="center">

🚀 **Convert YouTube and Bilibili videos into AI-powered Markdown notes** | **将 YouTube 和 Bilibili 视频转换为 AI 生成的 Markdown 笔记**

支持本地 Whisper 离线转录 + OpenRouter API 智能总结 | Supports local Whisper transcription + OpenRouter AI summarization

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

[English](#english) | [中文](#中文) | [快速开始](#-quick-start--快速开始) | [使用示例](#-usage-examples--使用示例) | [配置](#-configuration--配置)

</div>

---

## 🌐 Language | 语言

<div style="padding: 15px; background-color: #f0f0f0; border-radius: 8px;">

Click below to switch language | 点击下方切换语言：

- [🇺🇸 English](#english)
- [🇨🇳 中文](#中文)

</div>

---

## English

### What is Video-to-Notes?

Convert YouTube and Bilibili videos into structured AI-powered Markdown notes using local Whisper transcription (free) + OpenRouter API for summarization.

**Why use this?**
- 💰 **Cost-effective**: Free local transcription, only pay for AI summary (~$0.02-0.05 per video)
- 🔒 **Privacy-focused**: Audio processed locally, never leaves your machine
- 🌍 **Multi-platform**: YouTube, Bilibili
- ⚡ **Fast**: 2-3 minutes for an 8-minute video

### 🚀 Quick Start

#### 1. Install System Dependencies

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
# OR via package manager
# Windows: choco install yt-dlp
# macOS: brew install yt-dlp
```

#### 2. Setup Python Environment (with uv)

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
OUTPUT_DIRECTORY=./notes
TEMP_DIRECTORY=./temp
LOG_LEVEL=INFO
MAX_VIDEO_LENGTH=7200
```

**Get API Key**: Visit [OpenRouter.ai](https://openrouter.ai/), sign up, create API key, add credits ($5-10 is enough for hundreds of videos).

### 💻 Usage Examples

#### Standalone Script

```bash
# Basic usage
python process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# With language specification (e.g., Chinese)
python process_video.py --url "https://www.bilibili.com/video/BV1xx411c7XZ" --language zh

# Save to file
python process_video.py --url "https://..." --save-to-file --output-path "./my_notes"

# Use different AI model
python process_video.py --url "https://..." --ai-model "anthropic/claude-3.5-sonnet"

# Verbose logging
python process_video.py --url "https://..." --verbose
```

#### Claude Code Integration

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

### ⚙️ Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | ✅ Yes | - | OpenRouter API key for AI summarization |
| `AI_MODEL` | No | `anthropic/claude-3.5-sonnet` | AI model for summarization |
| `WHISPER_MODEL` | No | `base` | Whisper model size (tiny/base/small/medium/large) |
| `OUTPUT_DIRECTORY` | No | `./notes` | Output directory for saved notes |
| `TEMP_DIRECTORY` | No | `./temp` | Temporary directory for processing |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_VIDEO_LENGTH` | No | `7200` | Maximum video length in seconds (2 hours) |

**Recommended AI Models**:
- `google/gemini-2.5-flash` - Fast, low cost, good quality (Recommended)
- `anthropic/claude-3.5-sonnet` - Best quality, moderate cost
- `openai/gpt-4-turbo` - High quality, higher cost

**Whisper Models**:
- `tiny` (~1GB) - Fastest, basic accuracy
- `base` (~1GB) - **Recommended** - balanced performance
- `small` (~2GB) - Better accuracy, needs decent GPU
- `medium` (~5GB) - High quality
- `large` (~10GB) - Best quality, requires powerful hardware

### 📊 Output Example

```markdown
# Video Title

## Core Points | 核心要点
- Key point 1
- Key point 2
- Key point 3

## Detailed Summary | 详细总结
AI-generated detailed summary of the video content...

---
**Source | 来源**: https://www.youtube.com/watch?v=...
**Duration | 时长**: 0:08:45
**Author | 作者**: Channel Name
**Processed | 处理时间**: 2025-01-15 14:30:00
```

### ⚡ Performance

**Processing time (8-minute video, base model)**:
- Video download: ~7 seconds
- Audio extraction: ~1 second
- Local Whisper transcription: ~30-60 seconds (CPU) or ~10-20 seconds (GPU)
- AI summarization: ~5-6 seconds
- **Total: ~50-80 seconds (CPU) or ~25-35 seconds (GPU)**

**First run**: Downloads Whisper model (~150MB for base model)

### 💰 Cost

**Per 8-minute video**:
- Local Whisper transcription: **FREE** (uses your hardware)
- OpenRouter (Gemini 2.5 Flash): ~$0.02-0.05
- **Total: ~$0.02-0.05 per video**

---

## 中文

### 什么是 Video-to-Notes？

将 YouTube 和 Bilibili 视频转换为结构化的 AI 驱动 Markdown 笔记，使用本地 Whisper 转录（免费）+ OpenRouter API 进行总结。

**为什么使用这个？**
- 💰 **成本效益**: 本地转录免费，仅 AI 总结付费（约 $0.02-0.05/视频）
- 🔒 **隐私保护**: 音频本地处理，绝不离开你的机器
- 🌍 **多平台**: YouTube、Bilibili
- ⚡ **快速**: 8分钟视频只需2-3分钟

### 🚀 快速开始

#### 1. 安装系统依赖

**FFmpeg** (音频提取必需):
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

**yt-dlp** (视频下载必需):
```bash
# 全局安装为系统工具
pip install yt-dlp
# 或通过包管理器
# Windows: choco install yt-dlp
# macOS: brew install yt-dlp
```

#### 2. 设置 Python 环境（使用 uv）

```bash
# 克隆仓库
git clone https://github.com/Enyu-Liu/video-to-notes-skill.git
cd video-to-notes-skill/scripts

# 使用 uv 创建虚拟环境（推荐）
uv venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装 Python 依赖
uv pip install -r requirements.txt
```

**注意**: `yt-dlp` 在系统安装（用于 CLI）和 `requirements.txt`（用于 Python 导入）中都出现。两者都需要。

#### 3. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 并添加你的 OpenRouter API 密钥
```

**`.env` 配置**:
```env
# 必需：OpenRouter API 密钥（从 https://openrouter.ai/ 获取）
OPENROUTER_API_KEY=sk-or-your-key-here

# 可选配置
AI_MODEL=google/gemini-2.5-flash
WHISPER_MODEL=base
OUTPUT_DIRECTORY=./notes
TEMP_DIRECTORY=./temp
LOG_LEVEL=INFO
MAX_VIDEO_LENGTH=7200
```

**获取 API 密钥**: 访问 [OpenRouter.ai](https://openrouter.ai/)，注册账户，创建 API 密钥，充值（$5-10 足够处理数百个视频）。

### 💻 使用示例

#### 独立脚本

```bash
# 基础用法
python process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 指定语言（例如中文）
python process_video.py --url "https://www.bilibili.com/video/BV1xx411c7XZ" --language zh

# 保存到文件
python process_video.py --url "https://..." --save-to-file --output-path "./my_notes"

# 使用不同 AI 模型
python process_video.py --url "https://..." --ai-model "anthropic/claude-3.5-sonnet"

# 详细日志
python process_video.py --url "https://..." --verbose
```

#### Claude Code 集成

在 Claude Code 中直接使用技能：

```
/video-to-notes https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```
/video-to-notes https://www.bilibili.com/video/BV1LzqLBaE1B --language zh
```

```
/video-to-notes https://... --save-to-file --output-path ./notes
```

### ⚙️ 配置

| 变量 | 必需 | 默认值 | 描述 |
|------|------|--------|------|
| `OPENROUTER_API_KEY` | ✅ 是 | - | OpenRouter API 密钥（用于 AI 总结） |
| `AI_MODEL` | 否 | `anthropic/claude-3.5-sonnet` | 用于总结的 AI 模型 |
| `WHISPER_MODEL` | 否 | `base` | Whisper 模型大小 (tiny/base/small/medium/large) |
| `OUTPUT_DIRECTORY` | 否 | `./notes` | 笔记保存目录 |
| `TEMP_DIRECTORY` | 否 | `./temp` | 处理临时目录 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 (DEBUG, INFO, WARNING, ERROR) |
| `MAX_VIDEO_LENGTH` | 否 | `7200` | 最大视频长度（秒，2小时） |

**推荐 AI 模型**:
- `google/gemini-2.5-flash` - 快速、低成本、良好质量（推荐）
- `anthropic/claude-3.5-sonnet` - 最佳质量、中等成本
- `openai/gpt-4-turbo` - 高质量、较高成本

**Whisper 模型**:
- `tiny` (~1GB) - 最快，基础精度
- `base` (~1GB) - **推荐** - 平衡性能
- `small` (~2GB) - 更好精度，需要独显
- `medium` (~5GB) - 高质量
- `large` (~10GB) - 最佳质量，需要强大硬件

### 📊 输出示例

```markdown
# 视频标题

## 核心要点
- 要点 1
- 要点 2
- 要点 3

## 详细总结
AI 生成的详细总结内容...

---
**来源**: https://www.youtube.com/watch?v=...
**时长**: 0:08:45
**作者**: 频道名称
**处理时间**: 2025-01-15 14:30:00
```

### ⚡ 性能

**处理时间（8分钟视频，base 模型）**:
- 视频下载：~7 秒
- 音频提取：~1 秒
- 本地 Whisper 转录：~30-60 秒（CPU）或 ~10-20 秒（GPU）
- AI 总结：~5-6 秒
- **总计：~50-80 秒（CPU）或 ~25-35 秒（GPU）**

**首次运行**：下载 Whisper 模型（base 模型约 150MB）

### 💰 成本

**每个 8分钟视频**:
- 本地 Whisper 转录：**免费**（使用你的硬件）
- OpenRouter（Gemini 2.5 Flash）：~$0.02-0.05
- **总计：约 $0.02-0.05/视频**

---

## 🛠️ 技术架构 | Architecture

- **视频下载 | Video Download**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **音频提取 | Audio Extraction**: [FFmpeg](https://ffmpeg.org/)
- **语音转录 | Speech-to-Text**: [OpenAI Whisper](https://github.com/openai/whisper) (本地 | local)
- **AI 总结 | AI Summarization**: [OpenRouter](https://openrouter.ai/) (Claude/Gemini 等 | etc)
- **环境管理 | Env Management**: [uv](https://github.com/astral-sh/uv) (推荐 | recommended)

## 📜 许可证 | License

MIT License - 详见 [LICENSE](LICENSE) 文件 | See [LICENSE](LICENSE) file

## 🙏 致谢 | Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 视频下载 | Video download
- [FFmpeg](https://ffmpeg.org/) - 音频提取 | Audio extraction
- [OpenAI Whisper](https://github.com/openai/whisper) - 本地转录 | Local transcription
- [OpenRouter](https://openrouter.ai/) - AI 总结 | AI summarization

---

<div align="center">

⭐ **Star this repo if helpful!** | **如果有用请给个 Star！**

[⬆ Back to Top](#video-to-notes-skill--视频转笔记技能)

</div>
