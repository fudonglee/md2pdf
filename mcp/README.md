# 🤖 md2pdf MCP 集成指南

> 将 md2pdf 作为 MCP 工具接入 Codex、Cherry Studio、Cursor、WorkBuddy 等 AI 智能体。

## 工作原理

MCP (Model Context Protocol) 是一种让 AI 智能体调用外部工具的标准化协议。
md2pdf 启动一个 MCP 服务，智能体通过该服务调用 PDF 转换功能。

```
AI 智能体 (Codex/Cherry Studio)
        │
        │ MCP 协议调用
        ▼
┌──────────────────┐
│  md2pdf MCP Server │
│  (mcp/mcp-server.py)│
├──────────────────┤
│  md2pdf_convert    │  ← 转换文本 → base64 PDF
│  md2pdf_convert_file│  ← 转换文件 → PDF
└──────────────────┘
```

## 快速配置

### 通用配置格式

在智能体的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "md2pdf": {
      "command": "python",
      "args": ["/绝对路径/md2pdf/mcp/mcp-server.py"]
    }
  }
}
```

### 各平台配置位置

| 平台 | 配置方式 |
|------|---------|
| **Codex** | `~/.codex/config.toml` |
| **Cherry Studio** | 设置 → MCP 服务器 → 添加（见下方 Cherry Studio 专属配置） |
| **Cursor** | `.cursor/mcp.json` |
| **OpenCode** | `opencode.json` 中的 mcpServers |
| **Claude Desktop** | `claude_desktop_config.json` |
| **WorkBuddy** | 插件 MCP 配置 |

### Cherry Studio 专属配置

Cherry Studio 使用 UI 表单配置 MCP，打开 **设置 → MCP 服务器 → 添加**，填写：

| 字段 | 值 |
|------|-----|
| **类型** | `标准输入/输出（stdio）` |
| **名称** | `md2pdf` |
| **命令** | `python` |
| **参数**（一行一个） | `/绝对路径/md2pdf/mcp/mcp-server.py` |
| **环境变量** | 留空 |
| **是否支持长时间运行模式** | 可选（建议开启） |

> 参数行必须填 `mcp/mcp-server.py` 的**绝对路径**。
> 示例：`/Users/fudonglee/projects/md2pdf/mcp/mcp-server.py`

## 可用工具

### 1. `md2pdf_convert`

将 Markdown **文本** 转换为 PDF，返回 base64 编码的 PDF 内容。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `markdown` | string | ✅ | Markdown 文本内容 |
| `filename` | string | ❌ | 输出文件名（默认 output.pdf） |

### 2. `md2pdf_convert_file`

将 `.md` **文件** 转换为 `.pdf` 文件。

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input_path` | string | ✅ | 输入的 .md 文件路径 |
| `output_path` | string | ✅ | 输出的 .pdf 文件路径 |
| `toc` | boolean | ❌ | 生成目录 |
| `cover` | boolean | ❌ | 生成封面 |
| `title` | string | ❌ | 文档标题 |
| `author` | string | ❌ | 作者 |

## 示例：在 WorkBuddy 中调用

WorkBuddy 的智能体编排中，当需要将 Markdown 报告转为 PDF 时，MCP 服务会被自动调用：

```
用户: "把这份报告转成 PDF"
  → WorkBuddy 识别意图
  → 调用 md2pdf MCP 工具
  → md2pdf_convert_file 执行转换
  → PDF 文件生成并返回路径
```

## 手动测试 MCP 服务

```bash
# 启动 MCP 服务
python /path/to/md2pdf/mcp/mcp-server.py

# 服务会在 stdio 上监听 MCP 协议消息
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | `pip install 'md2pdf-tool[mcp]'` |
| 连接被拒绝 | 检查命令路径是否为绝对路径 |
| 中文显示异常 | 安装中文字体（Linux: `apt install fonts-noto-cjk`） |
