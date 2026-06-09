#!/usr/bin/env python3
"""
MCP Server for md2pdf — 将 md2pdf 作为 MCP 工具暴露给 AI 智能体。

启动方式:
    python mcp/mcp-server.py

找路径:
    在项目目录下执行: realpath mcp/mcp-server.py

通用 JSON 配置（Codex / Cursor / Claude Desktop / OpenCode）:
    {
        "mcpServers": {
            "md2pdf": {
                "command": "python3",
                "args": ["/chemin/vers/md2pdf/mcp/mcp-server.py"]
            }
        }
    }

Cherry Studio 配置（UI 表单）:
    类型: 标准输入/输出（stdio）
    名称: md2pdf
    命令: python3
    参数（一行一个）: /chemin/vers/md2pdf/mcp/mcp-server.py
    环境变量: 留空
    长时间运行模式: 建议开启
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from md2pdf.renderer import md_to_html
from md2pdf.i18n import DEFAULT_LANG

# ---------- MCP SDK ----------
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    HAS_MCP = True
except ImportError:
    HAS_MCP = False


TOOL_DEFINITIONS = [
    types.Tool(
        name="md2pdf_convert",
        description="Convert Markdown text to PDF (or HTML), returns base64-encoded file",
        inputSchema={
            "type": "object",
            "properties": {
                "markdown": {"type": "string", "description": "Markdown text content"},
                "filename": {"type": "string", "description": "Output filename (default: output.pdf)"},
                "output_format": {"type": "string", "description": "Output format: 'pdf' (default) or 'html'"},
                "lang": {"type": "string", "description": "Document language: 'zh-CN' (default) or 'en'"},
            },
            "required": ["markdown"],
        },
    ),
    types.Tool(
        name="md2pdf_convert_file",
        description="Convert .md file to .pdf (or .html) file",
        inputSchema={
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Input .md file path"},
                "output_path": {"type": "string", "description": "Output .pdf or .html file path"},
                "output_format": {"type": "string", "description": "Output format: 'pdf' (default) or 'html'"},
                "toc": {"type": "boolean", "description": "Generate table of contents"},
                "cover": {"type": "boolean", "description": "Generate cover page"},
                "title": {"type": "string", "description": "Document title"},
                "author": {"type": "string", "description": "Author"},
                "lang": {"type": "string", "description": "Document language: 'zh-CN' (default) or 'en'"},
            },
            "required": ["input_path", "output_path"],
        },
    ),
]


def _find_weasyprint() -> str | None:
    import shutil
    for p in ["/opt/anaconda3/bin/weasyprint"]:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    wp = shutil.which("weasyprint")
    if wp:
        return wp
    for p in ["/usr/local/bin/weasyprint", "/usr/bin/weasyprint", os.path.expanduser("~/.local/bin/weasyprint")]:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def html_to_pdf(html: str, output_path: str) -> bool:
    import subprocess
    wp = _find_weasyprint()
    if not wp:
        return False
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    try:
        tmp.write(html)
        tmp.close()
        r = subprocess.run([wp, tmp.name, output_path], capture_output=True, text=True, timeout=120)
        return r.returncode == 0
    except:
        return False
    finally:
        os.unlink(tmp.name)


def handle_convert(markdown: str, filename: str = "output.pdf", output_format: str = "pdf", lang: str = DEFAULT_LANG) -> list:
    html = md_to_html(md_text=markdown, lang=lang)
    if output_format == "html":
        return [types.TextContent(type="text", text=base64.b64encode(html.encode()).decode())]
    tmp = os.path.join(tempfile.gettempdir(), filename)
    ok = html_to_pdf(html, tmp)
    if not ok:
        return [types.TextContent(type="text", text="ERROR: PDF generation failed")]
    with open(tmp, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    os.unlink(tmp)
    return [types.TextContent(type="text", text=b64)]


def handle_convert_file(input_path: str, output_path: str, output_format: str = "pdf", toc: bool = False, cover: bool = False, title: str = "", author: str = "", lang: str = DEFAULT_LANG) -> list:
    md_text = Path(input_path).read_text(encoding="utf-8")
    html = md_to_html(md_text, toc=toc, cover=cover, title=title or Path(input_path).stem, author=author, lang=lang)
    if output_format == "html":
        Path(output_path).write_text(html, encoding="utf-8")
        size = Path(output_path).stat().st_size / 1024
        return [types.TextContent(type="text", text=f"OK: {output_path} ({size:.1f} KB)")]
    ok = html_to_pdf(html, output_path)
    if ok:
        size = Path(output_path).stat().st_size / 1024
        return [types.TextContent(type="text", text=f"OK: {output_path} ({size:.1f} KB)")]
    return [types.TextContent(type="text", text="ERROR: PDF generation failed")]


async def serve():
    server = Server("md2pdf")

    @server.list_tools()
    async def list_tools():
        return TOOL_DEFINITIONS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "md2pdf_convert":
            return handle_convert(**arguments)
        elif name == "md2pdf_convert_file":
            return handle_convert_file(**arguments)
        raise ValueError(f"Unknown tool: {name}")

    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(
            read, write,
            InitializationOptions(
                server_name="md2pdf",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    if not HAS_MCP:
        print("ERROR: mcp library required: pip install 'md2pdf-tool[mcp]'", file=sys.stderr)
        sys.exit(1)
    import asyncio
    asyncio.run(serve())


if __name__ == "__main__":
    main()
