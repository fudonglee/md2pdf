# 📄 md2pdf — Markdown / mrkdwn → 精美 PDF

> **把 Markdown 文档变成印刷级精美 PDF，一行命令搞定。**
> 兼容 CommonMark、GFM (GitHub Flavored Markdown) 和 Slack mrkdwn 格式。

<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-orange.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-macOS%20|%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/MCP-ready-purple.svg" alt="MCP">
</p>

---

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| **📝 格式兼容** | CommonMark、GFM（表格/任务列表/删除线）、Slack mrkdwn |
| **🌏 中文优化** | 思源宋体 / Noto Serif CJK 排版，两端对齐 |
| **🎨 代码高亮** | Pygments 语法高亮，支持 100+ 编程语言 |
| **📑 目录生成** | 自动从标题提取目录（`--toc`） |
| **📋 封面页** | 自动生成封面（`--cover`） |
| **📊 表格渲染** | 斑马条纹、表头深色背景 |
| **🔗 脚注支持** | 标准 Markdown 脚注 |
| **📦 管道输入** | 支持 `cat file.md \| md2pdf -o out.pdf` |
| **🤖 MCP 集成** | 可作为 Tool 接入 Codex、Cherry Studio、WorkBuddy |
| **🎯 零成本** | 开源免费，MIT License |

---

## 🚀 快速开始（30 秒）

### 安装

```bash
# 方式一：pip 安装（推荐）
pip install md2pdf-tool

# 方式二：一键脚本
curl -sSL https://raw.githubusercontent.com/fudonglee/md2pdf/main/scripts/install.sh | bash

# 方式三：本地安装
git clone https://github.com/fudonglee/md2pdf.git
cd md2pdf
pip install .
```

### 使用

```bash
# 基本转换
md2pdf 我的文档.md -o 我的文档.pdf

# 带目录和封面（推荐用于长文档）
md2pdf README.md -o README.pdf --toc --cover --title "项目文档" --author "作者"

# 管道模式
cat report.md | md2pdf -o report.pdf

# 自定义样式
md2pdf doc.md -o doc.pdf --font-size 10pt --paper-size A4
```

### 验证安装

```bash
md2pdf --version
# 输出: md2pdf 1.0.0
```

---

## 📖 完整使用指南

### 基本用法

```bash
md2pdf input.md -o output.pdf
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input.md` | 输入的 Markdown 文件（缺省从 stdin 读） | — |
| `-o output.pdf` | **必需** 输出的 PDF 文件路径 | — |
| `--toc` | 自动生成目录 | 关闭 |
| `--cover` | 生成封面页 | 关闭 |
| `--title "..."` | 文档标题（封面/HTML title） | 文件名 |
| `--author "..."` | 作者名称（封面） | 空 |
| `--font-size 12pt` | 基础字号 | 11pt |
| `--paper-size A4` | 纸张大小 | A4 |
| `--margin "2cm"` | 页边距 | 2.5cm 2cm |
| `--css custom.css` | 使用自定义 CSS 样式 | 内置样式 |
| `--lang zh-CN` | 界面与文档语言（支持 zh-CN, en） | zh-CN |
| `--debug` | 输出中间 HTML（调试用） | 关闭 |
| `--version` | 查看版本 | — |

### 常见场景

#### 📄 读书笔记 / 学习笔记

```bash
md2pdf 笔记.md -o 笔记.pdf --toc --cover --title "学习笔记"
```

#### 🐍 技术文档

```bash
md2pdf docs/api.md -o docs/api.pdf --toc --font-size 10pt
```

#### 📊 项目报告

```bash
md2pdf report.md -o report.pdf --toc --cover --title "季度报告" --author "张三"
```

#### 🔄 从网页抓取后转换

```bash
curl -s https://example.com/doc.md | md2pdf -o webpage.pdf
```

### 自定义 CSS

创建 `my-theme.css`，覆盖默认样式：

```css
/* 修改正文字体 */
html {
  font-family: "Georgia", serif;
  font-size: 12pt;
  color: #333;
}

/* 修改标题颜色 */
h1, h2, h3 {
  color: #2c3e50;
}

/* 修改表格样式 */
th {
  background: #3498db;
}
```

然后使用：

```bash
md2pdf input.md -o output.pdf --css my-theme.css
```

---

### 🌐 多语言支持

md2pdf 内置多语言（i18n）支持，默认语言为中文（zh-CN），可切换至英文（en）。

```bash
# 中文（默认）
md2pdf input.md -o output.pdf --toc --cover --title "文档标题"

# 英文
md2pdf input.md -o output.pdf --toc --cover --title "Document" --lang en
```

**语言切换效果：**

| 项目 | zh-CN（默认） | en |
|------|:------------:|:--:|
| CLI 帮助信息 | 中文 | English |
| 错误/进度提示 | 中文 | English |
| HTML `<html lang="">` | `zh-CN` | `en` |
| 正文字体 | 思源宋体 / Noto Serif CJK SC | Georgia / Times New Roman |
| 标题字体 | 思源黑体 / Noto Sans CJK SC | Helvetica Neue / Arial |
| 目录标题 | 目录 / Table of Contents | Table of Contents |
| 封面日期格式 | 2026-06-09 | June 09, 2026 |

**MCP 工具**同样支持 `lang` 参数，AI 智能体调用时可指定语言。

---

## 🎨 格式支持

| 格式类别 | 语法 | 支持 |
|---------|------|:----:|
| **标题** | `# H1` 到 `###### H6` | ✅ |
| **粗体** | `**text**` 或 `__text__` | ✅ |
| **斜体** | `*text*` 或 `_text_` | ✅ |
| **删除线** | `~~text~~` | ✅ |
| **行内代码** | `` `code` `` | ✅ |
| **链接** | `[text](url)` | ✅ |
| **图片** | `![alt](url)` | ✅ |
| **引用** | `> quote` | ✅ |
| **无序列表** | `- item` / `* item` | ✅ |
| **有序列表** | `1. item` | ✅ |
| **任务列表** | `- [x] task` | ✅ |
| **表格** | `\| col \| col \|` | ✅ |
| **代码块** | ```` ``` ```` | ✅ |
| **语法高亮** | ```` ```python ```` | ✅ |
| **脚注** | `[^1]` / `[^1]: text` | ✅ |
| **定义列表** | `term` / `: def` | ✅ |
| **分割线** | `---` / `***` | ✅ |
| **YAML 头** | `---` `title: ...` `---` | ✅ |
| **Slack 提及** | `<@U12345>` | ✅ |
| **Slack 链接** | `<url\|text>` | ✅ |

---

## 🤖 MCP 集成（AI 智能体调用）

md2pdf 可作为 **MCP (Model Context Protocol) 服务**运行，被 Codex、Cherry Studio、Cursor、WorkBuddy 等智能体调用。

### 配置方式

在智能体的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "md2pdf": {
      "command": "python",
      "args": ["/path/to/md2pdf/mcp/mcp-server.py"]
    }
  }
}
```

### 暴露的工具

| 工具名称 | 说明 |
|---------|------|
| `md2pdf_convert` | 将 Markdown 文本转换为 PDF（返回 base64） |
| `md2pdf_convert_file` | 将 `.md` 文件转换为 `.pdf` 文件（指定路径） |

### 在 Codex 中使用

在 Codex 的 `~/.codex/config.toml` 中添加：

```toml
[mcpServers.md2pdf]
command = "python"
args = ["/path/to/md2pdf/mcp/mcp-server.py"]
```

### 在 Cherry Studio 中使用

在 Cherry Studio 的 MCP 配置中添加相同的 JSON 配置。

### 在 WorkBuddy 中使用

在 WorkBuddy 的 MCP 设置中注册 md2pdf 服务端点即可。

---

## 🛠️ 技术栈

```
┌──────────────────────────────────────┐
│           md2pdf CLI / MCP           │
├──────────────────────────────────────┤
│  markdown-it-py (CommonMark + GFM)   │  ← Markdown 解析
├──────────────────────────────────────┤
│  mdit-py-plugins (扩展语法支持)       │  ← 脚注/定义列表/任务列表
├──────────────────────────────────────┤
│  Pygments (代码语法高亮)             │  ← 100+ 语言着色
├──────────────────────────────────────┤
│  WeasyPrint (HTML → PDF 渲染)        │  ← 印刷级 PDF
├──────────────────────────────────────┤
│  MCP Python SDK (AI 智能体接入)      │  ← MCP 协议
└──────────────────────────────────────┘
```

---

## 📦 安装方式详解

### macOS

**推荐**: `pip install md2pdf-tool`

如果 WeasyPrint 报 glib/pango 错误：

```bash
# 使用 conda 安装 weasyprint（推荐）
conda install -c conda-forge weasyprint

# 或使用 homebrew（需安装 homebrew）
# brew install glib pango gdk-pixbuf
# pip install weasyprint
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
pip install md2pdf-tool
```

### Windows

> Windows 支持需要安装 GTK 运行时，推荐在 WSL 中使用。

```bash
# 在 WSL (Ubuntu) 中:
sudo apt-get update && sudo apt-get install -y libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
pip install md2pdf-tool
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
RUN pip install md2pdf-tool
COPY docs /docs
CMD ["md2pdf", "/docs/input.md", "-o", "/docs/output.pdf"]
```

---

## 📁 项目结构

```
md2pdf/
├── README.md                  # 本文件
├── LICENSE                    # MIT 许可证
├── pyproject.toml             # Python 包配置
├── requirements.txt           # 依赖清单
├── scripts/
│   └── install.sh             # 一键安装脚本
├── mcp/
│   ├── mcp-server.py          # MCP 服务（AI 智能体接入）
│   └── README.md              # MCP 集成文档
├── md2pdf/                    # Python 源码包
│   ├── __init__.py
│   ├── __main__.py            # python -m md2pdf 入口
│   ├── cli.py                 # 命令行参数解析
│   ├── parser.py              # Markdown 解析引擎
│   ├── renderer.py            # HTML → PDF 渲染
│   ├── css.py                 # 印刷级 CSS 模板
│   └── utils.py               # 工具函数
└── samples/
    └── sample.md              # 示例文件
```

---

## 🧪 测试

```bash
# 使用示例文件测试
md2pdf samples/sample.md -o /tmp/sample.pdf --toc --cover --title "测试文档"
open /tmp/sample.pdf
```

---

## ⚠️ 常见问题

### Q: 生成的 PDF 中文显示空白？
确保系统安装了中文字体。macOS 内置「宋体」「苹方」，Linux 需要 `apt-get install fonts-noto-cjk`。

### Q: WeasyPrint 报错 "cannot load library"？
macOS 上需要使用 conda 安装 weasyprint，或安装 homebrew 后 `brew install glib pango gdk-pixbuf`。

### Q: 可以自定义 PDF 样式吗？
可以。使用 `--css my-theme.css` 传入自定义 CSS 文件。

### Q: 支持数学公式吗？
支持基础 LaTeX 数学公式（需启用 dollarmath 插件）。

### Q: 如何贡献？
提交 PR 或 Issue 到 GitHub 仓库。

---

## 📄 License

MIT License — 自由使用、修改、分发。

---

<p align="center">
  Made with ❤️ for the Markdown community
</p>
