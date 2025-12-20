# 🚀 5分钟快速开始

在 5 分钟内快速上手 video-to-notes！

## 📋 前置要求

- Python 3.10 或更高版本
- FFmpeg (音频处理)
- yt-dlp (视频下载)
- **推荐使用 uv** 进行 Python 环境管理

## 1️⃣ 安装系统依赖 (2分钟)

### 安装 FFmpeg
```bash
# Windows (使用 Chocolatey)
choco install ffmpeg

# macOS (使用 Homebrew)
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

### 安装 yt-dlp
```bash
# 使用 pip 安装
pip install yt-dlp
```

## 2️⃣ 设置 Python 环境 (2分钟)

```bash
# 克隆或进入项目目录
cd video-to-notes-skill

# 进入脚本目录
cd scripts

# 使用 uv 创建并激活虚拟环境 (推荐!)
uv venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装 Python 依赖
uv pip install -r requirements.txt
```

**💡 为什么使用 uv?**
- 更快的包安装速度
- 更好的依赖解析
- 现代化的 Python 环境管理

## 3️⃣ 获取 API Key (1分钟)

1. 访问 [OpenRouter.ai](https://openrouter.ai/)
   - 注册账户或登录
   - 创建 API Key
   - 复制 Key (格式: `sk-or-...`)
   - 充值少量费用 ($5-10 足够处理数百个视频)

**仅需这一个 API Key!**
- 本地 Whisper 转录 **完全免费** (无需 OpenAI Whisper API)
- 只需为 AI 总结付费

## 4️⃣ 配置环境变量 (30秒)

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Windows:
notepad .env
# macOS:
open -e .env
# Linux:
nano .env
```

在 `.env` 文件中设置：

```env
# OpenRouter API Key (必需)
OPENROUTER_API_KEY=sk-or-YOUR-KEY-HERE

# 可选配置
AI_MODEL=google/gemini-2.5-flash
WHISPER_MODEL=base
```

## 5️⃣ 测试运行 (30秒)

```bash
# 在 scripts 目录下执行
python process_video.py --url "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

你将看到：

```
Step 1/6: Downloading video from https://www.youtube.com/watch?v=jNQXAC9IVRw
✓ Video downloaded: Me at the zoo
  Duration: 0:00:18
  Platform: YouTube

Step 2/6: Extracting audio...
✓ Audio extracted: audio.m4a

Step 3/6: Transcribing audio with local Whisper (base)...
✓ Transcription completed (120 characters, language: en)

Step 4/6: Generating AI summary...
✓ Summary generated

Step 5/6: Formatting markdown...
✓ Markdown formatted (890 characters)

Step 6/6: Skipping file save

# Me at the zoo

## 核心要点
- First video ever uploaded to YouTube
- ...

---
**来源**: https://www.youtube.com/watch?v=jNQXAC9IVRw
**时长**: 0:00:18
**作者**: jawed
**处理时间**: 2025-01-15 14:30:00
```

## 🎉 完成!

现在你可以：

```bash
# 处理任何视频
python process_video.py --url "YOUR_VIDEO_URL"

# 保存到文件
python process_video.py --url "..." --save-to-file --output-path "./my_notes"

# 处理中文视频
python process_video.py --url "https://www.bilibili.com/video/..." --language zh

# 使用不同 AI 模型
python process_video.py --url "..." --ai-model "anthropic/claude-3.5-sonnet"
```

## 🔧 常见问题

### ❌ "OpenRouter API key is required"
- 确保 `.env` 文件在 `scripts/` 目录
- 检查 API Key 格式正确 (以 `sk-or-` 开头)

### ❌ "FFmpeg failed"
- 运行 `ffmpeg -version` 验证安装
- 安装 FFmpeg 后重启终端

### ❌ "Command not found: python"
- Windows 尝试使用 `py` 而不是 `python`
- Linux/macOS 使用 `python3`

### ❌ "uv: command not found"
- 安装 uv: https://github.com/astral-sh/uv
- 或者使用传统方式: `python -m venv .venv && source .venv/bin/activate`

### ❌ 转录速度慢
- 确保虚拟环境已激活
- 使用更小的模型: `WHISPER_MODEL=tiny`
- 首次运行需要下载模型 (~150MB)

## 💰 成本估算

**每个 8分钟视频:**
- 本地 Whisper 转录: **免费** (使用你的 CPU/GPU)
- OpenRouter (Gemini 2.5 Flash): ~$0.02-0.05
- **总计: ~$0.02-0.05/视频**

对比传统 API 方案: ~$0.07-0.10/视频

## 📚 下一步

1. 尝试处理你自己的视频
2. 使用 `--save-to-file` 保存笔记
3. 在 Claude Code 中使用 `/video-to-notes` 技能
4. 阅读 [README.md](README.md) 了解更多配置选项
5. 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 详细使用指南

## 🆘 需要帮助?

- 完整文档: 查看 [README.md](README.md)
- 详细使用指南: 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md)
- 故障排除: 查看 [README.md#故障排除](#故障排除) 部分
- 在 GitHub 提交 Issue

---

**🎯 小贴士**: 首次运行会下载 Whisper 模型，建议使用 `base` 模型平衡速度与精度!

祝您使用愉快! 📝
