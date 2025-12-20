# Video-to-Notes Skill

🚀 **在 Claude Code 中快速将 YouTube 和 Bilibili 视频转换为 AI 生成的 Markdown 笔记**

支持本地 Whisper 离线转录 + OpenRouter API 智能总结，无需担心 API 转录费用。

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ 特性

- 🎥 **多平台支持**: YouTube 和 Bilibili
- 🗣️ **本地 Whisper 转录**: 使用 OpenAI Whisper 进行离线语音识别
- 🤖 **AI 智能总结**: 通过 OpenRouter API (Claude、Gemini 等)
- 📝 **结构化 Markdown**: 标题、核心要点、详细总结、元数据
- 💰 **成本效益**: 免费本地转录，仅为 AI 总结付费

## 🚀 快速开始 (5分钟)

### 1️⃣ 安装系统依赖

#### FFmpeg (必需)
```bash
# Windows (使用 Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

#### yt-dlp (必需)
```bash
# 使用 pip 安装
pip install yt-dlp
```

### 2️⃣ 设置 Python 环境 (推荐使用 uv)

```bash
# 克隆仓库
git clone https://github.com/your-username/video-to-notes-skill.git
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

# 安装依赖
uv pip install -r requirements.txt
```

### 3️⃣ 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 OpenRouter API Key
# Windows:
notepad .env
# macOS:
open -e .env
# Linux:
nano .env
```

在 `.env` 文件中设置以下变量：

```env
# OpenRouter API Key (必需) - 从 https://openrouter.ai/ 获取
OPENROUTER_API_KEY=your_openrouter_api_key_here

# AI 模型选择 (可选)
AI_MODEL=google/gemini-2.5-flash

# Whisper 模型大小 (可选)
WHISPER_MODEL=base
```

**💡 获取 API Key:**
- 访问 [OpenRouter.ai](https://openrouter.ai/)
- 注册账户并创建 API Key
- 充值少量费用 ($5-10 足够处理数百个视频)

### 4️⃣ 测试运行

```bash
# 在 scripts 目录下执行
python process_video.py --url "https://www.bilibili.com/video/BV1LzqLBaE1B"
```

## 📖 使用说明

### 作为 Claude Skill 使用

在 Claude Code 中直接调用 `/video-to-notes` 技能：

```
/video-to-notes https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 命令行独立使用

```bash
# 基础用法
python process_video.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 指定语言 (例如中文)
python process_video.py --url "https://www.bilibili.com/video/BV1xx411c7XZ" --language zh

# 保存到文件
python process_video.py --url "https://..." --save-to-file --output-path "./my_notes"

# 使用不同的 AI 模型
python process_video.py --url "https://..." --ai-model "anthropic/claude-3.5-sonnet"

# 详细日志
python process_video.py --url "https://..." --verbose
```

## ⚙️ 配置选项

### 环境变量说明

| 变量 | 必需 | 默认值 | 描述 |
|------|------|--------|------|
| `OPENROUTER_API_KEY` | ✅ 是 | - | OpenRouter API Key (用于 AI 总结) |
| `AI_MODEL` | 否 | `anthropic/claude-3.5-sonnet` | AI 模型选择 |
| `WHISPER_MODEL` | 否 | `base` | Whisper 模型大小 (tiny/base/small/medium/large) |
| `OUTPUT_DIRECTORY` | 否 | `./notes` | 笔记保存目录 |
| `TEMP_DIRECTORY` | 否 | `./temp` | 临时文件目录 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 (DEBUG, INFO, WARNING, ERROR) |
| `MAX_VIDEO_LENGTH` | 否 | `7200` | 最大视频长度 (秒, 2小时) |

### Whisper 模型选择

根据你的硬件和精度需求选择：

| 模型 | 内存需求 | 速度 | 精度 | 推荐场景 |
|------|----------|------|------|----------|
| `tiny` | ~1GB | 最快 | 基础 | 快速预览、低配置硬件 |
| `base` | ~1GB | 快 | 良好 | **默认 - 平衡性能** |
| `small` | ~2GB | 中等 | 较好 | 一般用途，有独显 |
| `medium` | ~5GB | 慢 | 高 | 质量优先 |
| `large` | ~10GB | 最慢 | 最佳 | 专业转录 |

### 推荐 AI 模型

**AI 总结模型 (OpenRouter):**
- `google/gemini-2.5-flash` - 快速、低成本、良好质量 (**推荐**)
- `anthropic/claude-3.5-sonnet` - 最佳质量、中等成本
- `openai/gpt-4-turbo` - 高质量、较高成本

## 📊 输出示例

生成的 Markdown 笔记结构：

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

## ⚡ 性能表现

**处理时间 (8分钟视频, base 模型):**
- 视频下载: ~7 秒
- 音频提取: ~1 秒
- 本地 Whisper 转录: ~30-60 秒 (CPU) 或 ~10-20 秒 (GPU)
- AI 总结: ~5-6 秒
- **总计: ~50-80 秒 (CPU) 或 ~25-35 秒 (GPU)**

**注意**: 首次运行会下载 Whisper 模型 (~150MB, base 模型)

## 💰 成本估算

**8分钟视频成本:**
- 本地 Whisper 转录: **免费** (使用本地硬件)
- OpenRouter (Gemini 2.5 Flash): ~$0.02-0.05
- **总计: ~$0.02-0.05/视频**

对比 API 转录方案: ~$0.07-0.10/视频

## 🔧 故障排除

### ❌ "OpenRouter API key is required"
- 确保 `.env` 文件存在于 scripts 目录
- 检查 `OPENROUTER_API_KEY` 设置正确

### ❌ "FFmpeg failed"
- 验证 FFmpeg 安装: `ffmpeg -version`
- 检查视频是否下载成功

### ❌ "Failed to load Whisper model"
- 确保有足够 RAM/显存
- 尝试更小的模型 (例如 `WHISPER_MODEL=tiny`)
- 检查网络连接 (首次下载模型)

### 🔄 转录速度慢
- 使用更小模型 (`tiny` 或 `base`)
- 启用 GPU 加速 (如可用)
- 处理较短视频 (<10 分钟)

### ❌ "Video too long"
- 默认最大视频长度 2 小时 (7200 秒)
- 可在 `.env` 中调整 `MAX_VIDEO_LENGTH`

## ✅ 本地 Whisper 优势

**优势:**
- ✅ 转录 **无 API 费用** (仅 AI 总结付费)
- ✅ **无文件大小限制** (API 限制 25MB 音频)
- ✅ **离线工作** (模型下载后)
- ✅ **隐私保护** - 音频不会离开你的机器
- ✅ **无限使用** - 无 API 速率限制

**权衡:**
- ⚠️ 速度比 API 慢 (尤其在 CPU 上)
- ⚠️ 需要硬件支持大模型
- ⚠️ 首次运行下载模型 (~150MB - 3GB)

## 📁 项目结构

```
video-to-notes-skill/
├── scripts/
│   ├── process_video.py       # 主 CLI 脚本
│   ├── core/                  # 核心模块
│   │   ├── video_processor.py # yt-dlp + FFmpeg
│   │   ├── transcriber.py     # 本地 Whisper 模型
│   │   ├── summarizer.py      # OpenRouter API
│   │   └── exceptions.py
│   ├── config/
│   │   └── settings.py        # 配置管理
│   └── requirements.txt       # 依赖列表
├── .env.example               # 环境变量模板
├── .env                       # 你的配置 (被 git 忽略)
├── README.md                  # 说明文档
├── QUICK_START.md             # 快速开始指南
└── USAGE_GUIDE.md             # 详细使用指南
```

## 🛠️ 技术架构

- **视频下载**: yt-dlp
- **音频提取**: FFmpeg
- **语音转录**: OpenAI Whisper (本地模型)
- **AI 总结**: OpenRouter API (Claude/Gemini 等)
- **配置管理**: Pydantic Settings
- **环境管理**: uv (推荐)

## 📜 许可证

本项目基于 MIT 许可证开源，详情请查看 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 视频下载: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- 音频提取: [FFmpeg](https://ffmpeg.org/)
- 语音转录: [OpenAI Whisper](https://github.com/openai/whisper) (本地)
- AI 总结: [OpenRouter](https://openrouter.ai/)

## 📞 支持

如果你在使用过程中遇到问题，请：

1. 查看 [故障排除](#-故障排除) 部分
2. 查看 [QUICK_START.md](QUICK_START.md) 快速开始指南
3. 查看 [USAGE_GUIDE.md](USAGE_GUIDE.md) 详细使用说明
4. 在 GitHub 上提交 Issue

---

⭐ **如果这个项目对你有帮助，请给我们一个 Star!**
