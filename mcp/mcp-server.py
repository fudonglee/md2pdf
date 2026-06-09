#!/usr/bin/env python3
"""
MCP Server for md2pdf — 将 md2pdf 作为 MCP 工具暴露给 Codex、Cherry Studio 等智能体。

启动方式:
    python mcp/mcp-server.py

一般配置（Codex / Cursor / Claude Desktop / OpenCode）:
    {
        "mcpServers": {
            "md2pdf": {
                "command": "python",
                "args": ["/绝对路径/md2pdf/mcp/mcp-server.py"]
            }
        }
    }

Cherry Studio 配置（UI 表单）:
    类型: 标准输入/输出（stdio）
    名称: md2pdf
    命令: python
    参数（一行一个）: /绝对路径/md2pdf/mcp/mcp-server.py
    环境变量: 留空
    长时间运行模式: 建议开启

可用工具:
    - md2pdf_convert:      转换 Markdown 文本为 PDF/HTML，返回 base64
    - md2pdf_convert_file:  转换 .md 文件为 .pdf/.html 文件
"""

import json
import os
import sys
import base64
import tempfile
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from md2pdf.renderer import convert, convert_file, md_to_html
from md2pdf.i18n import lang_for

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    HAS_MCP = True
except ImportError:
    HAS_MCP = False


async def serve_mcp():
    server = Server("md2pdf")

    @server.list_tools()
    async def list_tools():
        return [
            types.Tool(
                name="md2pdf_convert",
                description="Convert Markdown text to PDF (or HTML), returns base64-encoded file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "markdown": {"type": "string", "description": "Markdown text content"},
                        "filename": {"type": "string", "description": "Output filename (optional, default output.pdf)"},
                        "output_format": {"type": "string", "description": "Output format: 'pdf' (default) or 'html'"},
                        "lang": {"type": "string", "description": "Document language (e.g. zh-CN, en), default zh-CN"},
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
                        "output_path": {"type": "string", "description": "Output file path"},
                        "output_format": {"type": "string", "description": "Output format: 'pdf' (default) or 'html'"},
                        "toc": {"type": "boolean", "description": "Generate table of contents"},
                        "cover": {"type": "boolean", "description": "Generate cover page"},
                        "title": {"type": "string", "description": "Document title"},
                        "author": {"type": "string", "description": "Author"},
                        "lang": {"type": "string", "description": "Document language (e.g. zh-CN, en), default zh-CN"},
                    },
                    "required": ["input_path", "output_path"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "md2pdf_convert":
            md_text = arguments["markdown"]
            filename = arguments.get("filename", "output.pdf")
            output_format = arguments.get("output_format", "pdf")
            lang = arguments.get("lang", "zh-CN")

            if output_format == "html":
                html = md_to_html(md_text, lang=lang)
                html_bytes = html.encode("utf-8")
                html_b64 = base64.b64encode(html_bytes).decode()
                return [types.TextContent(type="text", text=html_b64)]

            # Default: PDF
            tmp_path = os.path.join(tempfile.gettempdir(), filename)
            ok = convert(md_text, tmp_path, lang=lang)
            if not ok:
                return [types.TextContent(type="text", text=f"ERROR: PDF generation failed")]
            with open(tmp_path, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode()
            os.unlink(tmp_path)
            return [types.TextContent(type="text", text=pdf_b64)]

        elif name == "md2pdf_convert_file":
            input_path = arguments["input_path"]
            output_path = arguments["output_path"]
            output_format = arguments.get("output_format", "pdf")
            toc = arguments.get("toc", False)
            cover = arguments.get("cover", False)
            title = arguments.get("title", "")
            author = arguments.get("author", "")
            lang = arguments.get("lang", "zh-CN")

            if output_format == "html":
                from pathlib import Path as _Path
                md_text = _Path(input_path).read_text(encoding="utf-8")
                html = md_to_html(md_text, toc=toc, cover=cover, title=title, author=author, lang=lang)
                _Path(output_path).write_text(html, encoding="utf-8")
                size = len(html.encode("utf-8")) / 1024
                return [types.TextContent(type="text", text=f"OK: {output_path} ({size:.1f} KB)")]

            # Default: PDF
            ok = convert_file(
                input_path, output_path,
                toc=toc, cover=cover,
                title=title, author=author,
                lang=lang,
            )
            if ok:
                size = os.path.getsize(output_path) / 1024
                return [types.TextContent(type="text", text=f"OK: {output_path} ({size:.1f} KB)")]
            else:
                return [types.TextContent(type="text", text=f"ERROR: PDF generation failed")]

        raise ValueError(f"Unknown tool: {name}")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
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
    asyncio.run(serve_mcp())


if __name__ == "__main__":
    main()
