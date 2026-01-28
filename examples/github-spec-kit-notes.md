# GitHub Spec Kit：规范驱动开发工具详解与实践

**来源**: https://www.youtube.com/watch?v=a9eR1xsfvHg
**时长**: 0:40:00
**作者**: Den Delimarsky
**处理时间**: 2026-01-26 11:46:37

> **核心要点**
> 1. Spec Kit是GitHub推出的开源规范驱动开发工具包，旨在简化软件开发流程。
> 2. 它通过CLI工具或手动下载模板支持多种AI代理（如Copilot、Claude）和脚本类型（PowerShell、Shell）。
> 3. 核心概念包括"宪法文件"（Constitution），用于定义项目不可协商的原则和要求。
> 4. 开发流程遵循"规范（Spec）-计划（Plan）-任务（Task）"三阶段，逐步细化需求到可执行任务。
> 5. 强调将需求与技术实现分离，通过Markdown文件管理所有开发产物，易于团队协作和版本控制。
> 6. 支持迭代开发，可根据需要修改规范、切换AI模型并重新生成代码，实现快速原型和功能迭代。
> 7. 最终生成代码可直接运行，并提供可视化界面展示成果，验证规范驱动开发的有效性。

## 1. Spec Kit 简介与安装

**Spec Kit 核心理念**

Spec Kit 是 GitHub 推出的一个开源工具包，旨在通过规范驱动开发（Specification-Driven Development）简化软件构建过程。它帮助开发者摆脱"凭感觉编码"（vibe coding）的低效模式，通过明确的规范来指导AI生成代码，从而提高开发效率和软件质量。其核心思想是将"做什么"和"为什么做"与"如何做"分离，确保产品需求与技术实现解耦。

**安装与使用方式**

Spec Kit 可以通过两种主要方式使用：
1. **CLI 工具 (`specify CLI`)**：推荐使用 `uvx` 命令从 GitHub 仓库直接安装和运行，例如：`uvx github/spec-kit`。CLI 工具能自动化项目初始化、代理选择和脚本类型配置。
2. **手动下载模板**：用户可以直接从 GitHub Releases 页面下载预设的模板压缩包（针对不同的AI代理和脚本类型），然后将其解压到项目目录中。这种方式无需安装任何CLI工具，但需要手动配置。

**示例**：
- 使用 `uvx` 引导新项目：`uvx github/spec-kit podsite`，其中 `podsite` 是项目名称。
- 选择 AI 代理：在CLI交互界面中选择 `Copilot`、`Claude`、`Gemini` 或 `Cursor` 等。
- 选择脚本类型：根据操作系统选择 `PowerShell`（Windows）或 `Shell scripts`（Linux/WSL）。

## 2. 规范驱动开发流程

**项目初始化与宪法文件（Constitution）**

项目初始化后，Spec Kit 会生成一个 `specify` 文件夹，其中包含 `memory`、`scripts` 和 `templates` 等子目录。`memory` 目录下的 `constitution.md` 文件是项目的"宪法"，它定义了项目不可协商的原则和要求。例如，可以规定"必须包含测试"、"使用特定版本的 Next.js"等。AI 代理会参考此文件来生成代码。

**示例**：
通过 `/specify fill the constitution with the bare minimum requirements for a static web app based on a template` 命令，让 AI 填充宪法文件，例如：
```markdown
# Constitution for Podsite

## Article I: Static-First Delivery
- No server-side execution.
- Site ships HTML, CSS, JS, and static assets via CDN.

## Article II: Simplicity Over Tooling
- Prefer vanilla HTML, CSS, JS where possible.

## Article III: Accessibility and SEO Baseline
- All content must be accessible.
- Basic SEO best practices applied.
```

**定义规范（Spec）**

使用 `/specify` 命令定义项目的"做什么"和"为什么做"，而不是"如何做"。这一阶段专注于产品需求、用户场景和业务目标，不涉及具体技术栈。生成的规范文件（`specs/001-i-am-building.md`）是与实现无关的，便于团队理解和未来技术切换。

**示例**：
`/specify I am building a modern podcast website to look sleek. It should have a landing page with one featured episode, an episodes page, an about page, and an FAQ page. It should have 20 episodes, and the data is mocked.`

AI 会根据此描述生成详细的规范，包括用户故事、验收标准、功能需求和评审清单。评审清单会检查规范是否包含实现细节、是否需要澄清等。

**制定计划（Plan）**

使用 `/plan` 命令将高级规范转化为技术实现计划。这一阶段开始引入技术栈，但仍保持抽象。计划文件（`plans/001-i-am-building.md`）会包含技术上下文、主要依赖、测试策略、目标平台等。AI 在生成计划时会参考宪法文件和已定义的规范。

**示例**：
`/plan Use Next.js with static site configuration. No databases. Make sure the site is responsive and ready for mobile.`

AI 生成的计划可能包含：
- **技术栈**：JavaScript, TypeScript, Node.js, Next.js (SSG)
- **测试**：Lighthouse, Jest
- **部署**：CDN, Vercel, GitHub Pages, Azure Static Web Apps
- **架构**：静态优先，最小化依赖

**分解任务（Tasks）与代码生成**

使用 `/tasks` 命令将计划分解为可执行的、原子性的开发任务。这些任务会以 Markdown 文件的形式呈现，指导AI逐步完成代码实现。任务列表可以进行手动调整，例如调整测试优先顺序或移除不必要的步骤。

**示例**：
`/tasks Break this down.`

AI 生成的任务列表可能包括：
- **设置**：初始化 Next.js 应用骨架。
- **测试**：编写测试，确保测试失败（TDD）。
- **核心实现**：实现数据模型、页面布局（如关于页面、FAQ页面）。
- **集成与优化**：运行 Lighthouse 性能测试。
- **完善**：响应式图片、文档、可访问性优化。

最后，通过切换到适合代码生成的AI模型（如 `Cloud Sonnet 4`）并执行 `/implement the tasks for this project and update the task list as you go` 命令，AI 将根据任务列表逐步生成代码，并实时更新任务状态。

## 3. 成果展示与迭代优化

**代码生成与运行**

AI 完成任务后，会在项目目录中生成完整的代码。用户可以通过 `npm run build` 构建静态站点，然后通过 `npm run dev` 在本地运行查看效果。视频中展示了一个生成的播客网站，包含主页、关于页面、FAQ页面和剧集列表，证明了Spec Kit能够从高层规范直接生成可用的代码。

**示例**：
```bash
npm run build
npm run dev
```
访问 `localhost:3000` 即可查看生成的网站。

**迭代与定制化**

Spec Kit 的优势在于其高度可定制和可迭代性。所有开发产物（规范、计划、任务、宪法）都以 Markdown 文件形式存在，用户可以随时手动编辑这些文件来调整需求或技术细节。如果对AI生成的代码不满意，可以修改规范或计划，然后切换AI模型（例如从 `GPT-5` 切换到 `Sonnet 4`），并重新运行任务来生成新的代码。这种方式使得在项目生命周期中添加新功能、修复bug或调整设计变得更加结构化和高效。

**示例**：
如果生成的网站缺少页眉和页脚，可以直接编辑 `spec.md` 文件，添加"网站必须包含全局页眉和页脚"的需求，然后重新运行 `/implement` 命令，AI 将根据更新后的规范重新生成代码。
