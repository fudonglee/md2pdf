#!/usr/bin/env python3
"""
MCP Server for md2pdf — 将 md2pdf 作为 MCP 工具暴露给 AI 智能体。

启动方式:
    python mcp/mcp-server.py

本机绝对路径:
    /Users/lifudong/projects/md2pdf/mcp/mcp-server.py

通用 JSON 配置（Codex / Cursor / Claude Desktop / OpenCode）:
    {
        "mcpServers": {
            "md2pdf": {
                "command": "python3",
                "args": ["/Users/lifudong/projects/md2pdf/mcp/mcp-server.py"]
            }
        }
    }

Cherry Studio 配置（UI 表单）:
    类型: 标准输入/输出（stdio）
    名称: md2pdf
    命令: python3   ← 注意用 python3 不是 python
    参数（一行一个）: /Users/lifudong/projects/md2pdf/mcp/mcp-server.py
    环境变量: 留空
    长时间运行模式: 建议开启
"""

import base64
import os
import sys
import tempfile
from pathlib import Path

# 确保能找到项目包（无论工作目录在哪）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from md2pdf.renderer import md_to_html, convert
from md2pdf.i18n import DEFAULT_LANG

# ---------- MCP SDK ----------
try:
    from mcp.server.fastmcp import FastMCP
    HAS_MCP = True
except ImportError:
    HAS_MCP = False


def create_server():
    """Create and configure the MCP server with all tools."""
    mcp = FastMCP(
        "md2pdf",
        instructions="Convert Markdown to PDF/HTML. Supports Chinese and English.",
    )

    @mcp.tool()
    def md2pdf_convert(
        markdown: str,
        filename: str = "output.pdf",
        output_format: str = "pdf",
        lang: str = DEFAULT_LANG,
    ) -> str:
        """Convert Markdown text to PDF (or HTML), returns base64-encoded file.

        Args:
            markdown: Markdown text content
            filename: Output filename (default: output.pdf)
            output_format: Output format - 'pdf' (default) or 'html'
            lang: Document language - 'zh-CN' (default) or 'en'
        """
        html = md_to_html(md_text=markdown, lang=lang)

        if output_format == "html":
            html_bytes = html.encode("utf-8")
            return base64.b64encode(html_bytes).decode()

        # Generate PDF
        tmp_path = os.path.join(tempfile.gettempdir(), filename)
        import md2pdf.renderer as r
        ok = html_to_pdf_with_path(html, tmp_path)
        if not ok:
            return "ERROR: PDF generation failed"
        with open(tmp_path, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode()
        os.unlink(tmp_path)
        return pdf_b64

    @mcp.tool()
    def md2pdf_convert_file(
        input_path: str,
        output_path: str,
        output_format: str = "pdf",
        toc: bool = False,
        cover: bool = False,
        title: str = "",
        author: str = "",
        lang: str = DEFAULT_LANG,
    ) -> str:
        """Convert .md file to .pdf (or .html) file.

        Args:
            input_path: Input .md file path
            output_path: Output .pdf or .html file path
            output_format: Output format - 'pdf' (default) or 'html'
            toc: Generate table of contents
            cover: Generate cover page
            title: Document title
            author: Author name
            lang: Document language - 'zh-CN' (default) or 'en'
        """
        md_text = Path(input_path).read_text(encoding="utf-8")
        html = md_to_html(md_text, title=title or Path(input_path).stem, lang=lang)

        if output_format == "html":
            Path(output_path).write_text(html, encoding="utf-8")
            size = Path(output_path).stat().st_size / 1024
            return f"OK: {output_path} ({size:.1f} KB)"

        ok = html_to_pdf_with_path(html, output_path)
        if ok:
            size = Path(output_path).stat().st_size / 1024
            return f"OK: {output_path} ({size:.1f} KB)"
        return "ERROR: PDF generation failed"

    return mcp


def html_to_pdf_with_path(html: str, output_path: str) -> bool:
    """Convert HTML string to PDF using WeasyPrint."""
    import subprocess

    wp = _find_weasyprint()
    if not wp:
        print("ERROR: weasyprint not found", file=sys.stderr)
        return False

    tmp_html = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    try:
        tmp_html.write(html)
        tmp_html.close()
        result = subprocess.run(
            [wp, tmp_html.name, output_path],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return False
        return True
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False
    finally:
        os.unlink(tmp_html.name)


def _find_weasyprint() -> str | None:
    import shutil

    known_good = ["/opt/anaconda3/bin/weasyprint"]
    for p in known_good:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p

    wp = shutil.which("weasyprint")
    if wp:
        return wp

    fallbacks = [
        "/usr/local/bin/weasyprint",
        "/usr/bin/weasyprint",
        os.path.expanduser("~/.local/bin/weasyprint"),
    ]
    for p in fallbacks:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def main():
    if not HAS_MCP:
        print("ERROR: mcp library required: pip install 'md2pdf-tool[mcp]'", file=sys.stderr)
        sys.exit(1)

    mcp = create_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
