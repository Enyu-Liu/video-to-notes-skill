# 🎬 Video-to-Notes Skill

> 只需和 Claude 对话，就能将任何 YouTube/Bilibili 视频转换为结构化的 AI 笔记。

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[English](README.md)

---

## ✨ 能做什么

在 Claude Code 里发个视频链接，就能得到：
- **结构化 Markdown 笔记**，包含核心要点、章节、代码示例
- **智能格式化**技术内容（命令、代码块、示例）
- **隐私优先**的处理方式 - 音频不会离开你的电脑
- **超低成本** - 每个视频约 ¥0.14（仅 AI 总结需要付费）

**适用于：**教程视频、技术演讲、课程讲座、文档视频

---

## 🚀 快速安装

### 第 1 步：安装依赖

**系统要求：**
- [FFmpeg](https://ffmpeg.org/download.html) - 用于音频提取
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - `pip install yt-dlp`

**Python 依赖：**
```bash
cd scripts
pip install -r requirements.txt
```

### 第 2 步：获取 API 密钥

1. 访问 [OpenRouter.ai](https://openrouter.ai/)
2. 注册并创建 API 密钥
3. 充值 $5-10（足够处理 200+ 个视频）

### 第 3 步：配置

```bash
cp .env.example .env
# 编辑 .env，添加：OPENROUTER_API_KEY=sk-or-your-key-here
```

**搞定！**现在可以使用了。

---

## 💬 如何使用

### 在 Claude Code 中（推荐）

直接用自然语言和 Claude 对话：

**中文对话：**
```
请将这个视频转换为笔记：https://www.bilibili.com/video/BV1xx411c7XZ
```

```
帮我总结这个教程，用中文
```

```
把笔记保存到我的桌面/notes 文件夹
```

**English:**
```
Convert this video to notes: https://www.youtube.com/watch?v=a9eR1xsfvHg
```

```
Summarize this tutorial in English
```

```
Save the notes to my Documents folder
```

**Claude 会自动：**
1. ✅ 检查你的环境配置
2. ✅ 下载并处理视频
3. ✅ 生成精美的 Markdown 笔记
4. ✅ 如果你要求，会保存到文件

---

## 📊 输出效果

查看真实示例：[examples/github-spec-kit-notes.md](examples/github-spec-kit-notes.md)

**每个笔记包含：**
- 基于视频内容的清晰标题
- 视频元数据（来源、时长、作者、处理时间）
- 核心要点总结（3-7 条）
- 层次分明的章节结构
- 技术术语使用 `行内代码` 格式
- 带语法高亮的代码示例
- 复杂概念会配有智能示例

---

## 🎯 功能特性

| 功能 | 说明 |
|------|------|
| **支持平台** | YouTube、Bilibili、小红书 |
| **支持语言** | 自动检测，或指定：中文、英文、日文等 |
| **视频长度** | 最长 2 小时（可配置） |
| **处理速度** | 8 分钟视频约 2-3 分钟处理完成 |
| **成本** | 每个视频 ~$0.02-0.05（仅 AI 总结收费） |
| **隐私保护** | 使用 Whisper 本地处理音频 |

**可用的 AI 模型：**
- `google/gemini-2.5-flash`（默认 - 快速且便宜）
- `anthropic/claude-3.5-sonnet`（质量最佳）
- `openai/gpt-4-turbo`（平衡选择）

---

## ⚙️ 高级配置

### 环境变量（可选）

编辑 `.env` 进行自定义：

```env
# 必需
OPENROUTER_API_KEY=sk-or-your-key-here

# 可选 - 如需自定义可修改
AI_MODEL=google/gemini-2.5-flash    # 使用哪个 AI
WHISPER_MODEL=base                   # Whisper 模型：tiny/base/small/medium/large
DEFAULT_LANGUAGE=zh                  # 默认语言：zh/en/auto
OUTPUT_DIRECTORY=.                   # 笔记保存位置
```

### Whisper 模型选择

| 模型 | 速度 | 准确度 | 内存 | 适用场景 |
|------|------|--------|------|----------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | 1GB | 快速草稿 |
| `base` | ⚡⚡ | ⭐⭐⭐ | 1GB | **默认** - 平衡 |
| `small` | ⚡ | ⭐⭐⭐⭐ | 2GB | 更高准确度 |
| `medium` | 🐌 | ⭐⭐⭐⭐⭐ | 5GB | 高质量 |

---

## 🛠️ 开发者选项

### 架构

```
视频链接 → yt-dlp → FFmpeg → Whisper（本地）→ OpenRouter API → Markdown
```

### 命令行使用

如果你喜欢直接运行脚本：

```bash
python scripts/process_video.py \
  --url "https://www.youtube.com/watch?v=..." \
  --language zh \
  --save-to-file \
  --output-path "./notes"
```

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

<div align="center">

**基于** [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [FFmpeg](https://ffmpeg.org/) · [OpenAI Whisper](https://github.com/openai/whisper) · [OpenRouter](https://openrouter.ai/)

⭐ 如果有帮助，请给个 Star！

</div>
