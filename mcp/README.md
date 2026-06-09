# 🤖 md2pdf MCP 集成指南

> 将 md2pdf 作为 MCP 工具接入 Codex、Cherry Studio、Cursor、WorkBuddy 等 AI 智能体。

## 先找对路径（重要）

所有配置中的 `mcp/mcp-server.py` 路径都必须填**绝对路径**。

```bash
# 在项目目录下执行，拿到真实路径
realpath mcp/mcp-server.py
```

把输出的完整路径替换到下文所有示例中的 `/path/to/md2pdf` 部分。

## 工作原理

MCP (Model Context Protocol) 是一种让 AI 智能体调用外部工具的标准化协议。
md2pdf 启动一个 MCP 服务，智能体通过该服务调用 PDF/HTML 转换功能。

```
AI 智能体 (Codex/Cherry Studio/Cursor/WorkBuddy)
        │
        │ MCP 协议调用（stdio）
        ▼
┌────────────────────┐
│  md2pdf MCP Server  │
│  (mcp/mcp-server.py)│
├────────────────────┤
│  md2pdf_convert      │  ← 转换文本 → base64 PDF/HTML
│  md2pdf_convert_file │  ← 转换文件 → .pdf/.html
└────────────────────┘
```

## 各平台配置

### 通用 JSON 格式（Codex / Cursor / Claude Desktop / OpenCode）

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

### Codex（TOML 格式）

文件位置：`~/.codex/config.toml`

```toml
[mcpServers.md2pdf]
command = "python"
args = ["/path/to/md2pdf/mcp/mcp-server.py"]
```

### Cherry Studio（UI 表单）

打开 **设置 → MCP 服务器 → 添加**，逐项填写：

| 字段 | 值 |
|------|-----|
| **类型** | `标准输入/输出（stdio）` |
| **名称** | `md2pdf` |
| **命令** | `python` |
| **参数**（一行一个） | `/path/to/md2pdf/mcp/mcp-server.py` |
| **环境变量** | 留空 |
| **是否支持长时间运行模式** | 可选（建议开启） |

### WorkBuddy

在 WorkBuddy 的 MCP 工具配置中注册，命令填写：

```
python3 /path/to/md2pdf/mcp/mcp-server.py
```

## 可用工具

### 1. `md2pdf_convert`

将 Markdown **文本** 转换为 PDF 或 HTML，返回 base64 编码的文件内容。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `markdown` | string | ✅ | Markdown 文本内容 |
| `filename` | string | ❌ | 输出文件名（默认 output.pdf） |
| `output_format` | string | ❌ | 输出格式：`"pdf"`（默认）或 `"html"` |
| `lang` | string | ❌ | 文档语言：`"zh-CN"`（默认）或 `"en"` |

### 2. `md2pdf_convert_file`

将 `.md` **文件** 转换为 `.pdf` 或 `.html` 文件。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input_path` | string | ✅ | 输入的 .md 文件路径 |
| `output_path` | string | ✅ | 输出的 .pdf/.html 文件路径 |
| `output_format` | string | ❌ | 输出格式：`"pdf"`（默认）或 `"html"` |
| `toc` | boolean | ❌ | 生成目录 |
| `cover` | boolean | ❌ | 生成封面 |
| `title` | string | ❌ | 文档标题 |
| `author` | string | ❌ | 作者 |
| `lang` | string | ❌ | 文档语言：`"zh-CN"`（默认）或 `"en"` |

## 手动测试 MCP 服务

```bash
# 启动 MCP 服务（stdio 模式，等待 MCP 协议消息）
python3 /path/to/md2pdf/mcp/mcp-server.py

# 或在项目目录下用相对路径
# python mcp/mcp-server.py
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | `pip install 'md2pdf-tool[mcp]'` |
| 连接被拒绝 / 启动失败 | 检查 `mcp-server.py` 路径是否为**绝对路径** |
| 中文显示异常 | 安装中文字体（macOS 内置，Linux: `apt install fonts-noto-cjk`） |
| WeasyPrint 报错 | macOS 建议用 conda 安装：`conda install -c conda-forge weasyprint` |
