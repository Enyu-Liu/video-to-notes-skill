# Video-to-Notes Skill | 视频转笔记技能

<div align="center">

🚀 **将 YouTube 和 Bilibili 视频转换为 AI 生成的 Markdown 笔记**

本地 Whisper 转录 + OpenRouter API 智能总结

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

🌐 **其他语言**: [English](README.md)

</div>

---

## 什么是 Video-to-Notes？

将 YouTube 和 Bilibili 视频转换为结构化的 AI 驱动 Markdown 笔记，使用本地 Whisper 转录（免费）+ OpenRouter API 进行总结。

**为什么使用这个？**
- 💰 **成本效益**: 本地转录免费，仅 AI 总结付费（约 $0.02-0.05/视频）
- 🔒 **隐私保护**: 音频本地处理，绝不离开你的机器
- 🌍 **多平台**: YouTube、Bilibili
- ⚡ **快速**: 8分钟视频只需2-3分钟

## 🚀 快速开始

### 1. 安装系统依赖

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
```

### 2. 设置 Python 环境（使用 uv）

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

### 3. 配置环境

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

## 💻 使用方法

### Claude Code 集成

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

## ⚙️ 参数说明

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `url` | string | ✅ 是 | 视频链接（YouTube 或 Bilibili） | `https://www.youtube.com/watch?v=...`<br>`https://www.bilibili.com/video/BV...` |
| `--language` | string | 否 | 转录语言代码 | `zh` (中文)<br>`en` (英文)<br>`ja` (日语)<br>`ko` (韩语)<br>`auto` (自动检测) |
| `--ai-model` | string | 否 | 用于总结的 AI 模型 | `google/gemini-2.5-flash` (推荐)<br>`anthropic/claude-3.5-sonnet`<br>`openai/gpt-4-turbo` |
| `--save-to-file` | flag | 否 | 将输出保存到 markdown 文件 | `--save-to-file` |
| `--output-path` | string | 否 | 输出目录路径 | `./my_notes`<br>`../notes`<br>`/path/to/notes` |
| `--verbose` | flag | 否 | 启用详细日志 | `--verbose` |

### 语言选项

| 代码 | 语言 | 示例用法 |
|------|------|----------|
| `auto` | 自动检测（默认） | `--language auto` |
| `zh` | 中文 | `--language zh` |
| `en` | English | `--language en` |
| `ja` | 日本語 | `--language ja` |
| `ko` | 한국어 | `--language ko` |
| `es` | Español | `--language es` |
| `fr` | Français | `--language fr` |
| `de` | Deutsch | `--language de` |

### AI 模型选项

| 模型 | 提供商 | 速度 | 成本 | 质量 | 适用场景 |
|------|--------|------|------|------|----------|
| `google/gemini-2.5-flash` | Google | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | **推荐** - 快速、经济 |
| `anthropic/claude-3.5-sonnet` | Anthropic | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 最佳质量，详细分析 |
| `openai/gpt-4-turbo` | OpenAI | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | 高质量，平衡 |

### 输出路径选项

| 路径类型 | 示例 | 说明 |
|----------|------|------|
| 相对路径 | `./notes` | 相对于 `scripts/` 目录 |
| 相对路径 | `../my_notes` | 上级目录 |
| 绝对路径 | `/Users/name/Desktop/notes` | 完整系统路径 |
| 自定义 | `./output/video_notes` | 自定义子目录 |

## 📊 输出示例

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

## ⚙️ 配置参考

### 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `OPENROUTER_API_KEY` | ✅ 是 | - | OpenRouter API 密钥（用于 AI 总结） |
| `AI_MODEL` | 否 | `anthropic/claude-3.5-sonnet` | 用于总结的 AI 模型 |
| `WHISPER_MODEL` | 否 | `base` | Whisper 模型大小 (tiny/base/small/medium/large) |
| `OUTPUT_DIRECTORY` | 否 | `./notes` | 笔记保存目录 |
| `TEMP_DIRECTORY` | 否 | `./temp` | 处理临时目录 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 (DEBUG, INFO, WARNING, ERROR) |
| `MAX_VIDEO_LENGTH` | 否 | `7200` | 最大视频长度（秒，2小时） |

### Whisper 模型

| 模型 | 大小 | 内存/显存 | 速度 | 精度 | 推荐场景 |
|------|------|----------|------|------|----------|
| `tiny` | ~39 MB | ~1 GB | 最快 | 基础 | 快速预览、低配置硬件 |
| `base` | ~74 MB | ~1 GB | 快 | 良好 | **默认** - 平衡性能 |
| `small` | ~244 MB | ~2 GB | 中等 | 较好 | 一般用途，有独显 |
| `medium` | ~769 MB | ~5 GB | 慢 | 高 | 质量优先 |
| `large` | ~1550 MB | ~10 GB | 最慢 | 最佳 | 专业转录 |

## ⚡ 性能

**处理时间（8分钟视频，base 模型）**:
- 视频下载：~7 秒
- 音频提取：~1 秒
- 本地 Whisper 转录：~30-60 秒（CPU）或 ~10-20 秒（GPU）
- AI 总结：~5-6 秒
- **总计：~50-80 秒（CPU）或 ~25-35 秒（GPU）**

**首次运行**：下载 Whisper 模型（base 模型约 150MB）

## 💰 成本

**每个 8分钟视频**:
- 本地 Whisper 转录：**免费**（使用你的硬件）
- OpenRouter（Gemini 2.5 Flash）：~$0.02-0.05
- **总计：约 $0.02-0.05/视频**

## 🛠️ 技术架构

- **视频下载**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **音频提取**: [FFmpeg](https://ffmpeg.org/)
- **语音转录**: [OpenAI Whisper](https://github.com/openai/whisper) (本地)
- **AI 总结**: [OpenRouter](https://openrouter.ai/) (Claude/Gemini 等)
- **环境管理**: [uv](https://github.com/astral-sh/uv) (推荐)

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 视频下载
- [FFmpeg](https://ffmpeg.org/) - 音频提取
- [OpenAI Whisper](https://github.com/openai/whisper) - 本地转录
- [OpenRouter](https://openrouter.ai/) - AI 总结

---

<div align="center">

⭐ **如果有用请给个 Star！**

[⬆ 返回顶部](#video-to-notes-skill--视频转笔记技能)

</div>
