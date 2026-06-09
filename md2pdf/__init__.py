"""
md2pdf — Markdown / mrkdwn → 精美 PDF 转换工具。

兼容 CommonMark、GFM (GitHub Flavored Markdown) 和 Slack mrkdwn 格式。
支持表格、任务列表、代码语法高亮、脚注、定义列表、YAML front matter、LaTeX 数学公式。

完整文档: https://github.com/fudonglee/md2pdf
"""

__version__ = "1.0.0"
__author__ = "fudonglee"
__license__ = "MIT"

# Public API — explicitly exported for programmatic use
from .renderer import (
    md_to_html,          # Markdown → HTML string
    md_to_html_file,     # Markdown → save .html file
    convert_to_html,     # Alias: Markdown → HTML string
    convert,             # Markdown → output file (PDF or HTML)
    convert_file,        # .md file → output file (PDF or HTML)
    html_to_pdf,         # HTML string → .pdf file (low-level)
)
from .css import get_css        # Language-aware CSS
from .i18n import Lang, lang_for # Internationalization
