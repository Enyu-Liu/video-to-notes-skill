# Video-to-Notes Skill

将 YouTube/Bilibili 视频转换为 AI 生成的 Markdown 笔记。

本地 Whisper 转录（免费）+ OpenRouter API 总结（约 $0.02/视频）

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[English](README.md)

## 特性

- **成本低廉**: 本地转录免费，仅 AI 总结付费
- **隐私保护**: 音频本地处理
- **多平台支持**: YouTube、Bilibili、小红书

## 快速开始

### 1. 安装依赖

```bash
# 系统依赖
# - FFmpeg: https://ffmpeg.org/download.html
# - yt-dlp: pip install yt-dlp

# Python 依赖
cd scripts
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
cp .env.example .env
# 编辑 .env，添加 OpenRouter API 密钥
```

从 [OpenRouter.ai](https://openrouter.ai/) 获取 API 密钥

### 3. 运行

```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --language zh --save-to-file
```

## 使用方法

### 在 Claude Code 中

```
请将这个视频转换为笔记：https://www.youtube.com/watch?v=...
```

```
请将这个Bilibili视频转换为中文笔记：https://www.bilibili.com/video/BV...
```

### 命令行

```bash
# 基础用法
python scripts/process_video.py --url "VIDEO_URL"

# 完整选项
python scripts/process_video.py \
  --url "VIDEO_URL" \
  --language zh \
  --save-to-file \
  --output-path "./notes"
```

**参数说明：**
- `--url` - 视频链接（必需）
- `--language` - 语言代码：`zh`、`en`、`auto`
- `--ai-model` - AI 模型（默认：`google/gemini-2.5-flash`）
- `--save-to-file` - 保存为 Markdown 文件
- `--output-path` - 输出目录

## 输出示例

查看 [examples/github-spec-kit-notes.md](examples/github-spec-kit-notes.md) 获取真实输出示例。

**格式特性：**
- 结构化章节，包含核心要点摘要
- 代码格式化，支持语法高亮
- 对复杂概念提供智能示例

## 配置

**`.env` 文件：**

```env
OPENROUTER_API_KEY=sk-or-your-key-here  # 必需
AI_MODEL=google/gemini-2.5-flash        # 可选
WHISPER_MODEL=base                       # 可选：tiny/base/small/medium/large
DEFAULT_LANGUAGE=zh                      # 可选：zh/en/auto
```

## 架构

```
视频 URL → yt-dlp → FFmpeg → Whisper (本地) → OpenRouter API → Markdown
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
