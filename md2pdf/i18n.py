"""
Internationalization (i18n) support for md2pdf.

Provides translation dictionaries, language resolution, and font configuration
for multiple languages. Default language is zh-CN (Chinese Simplified).

Adding a new language:
    1. Add a new entry to LANGUAGES dict with all required keys
    2. Add canonical mappings in SUPPORTED_LANGS dict
"""

import textwrap

LANGUAGES = {
    "zh-CN": {
        "code": "zh-CN",
        "name": "中文",
        "html_lang": "zh-CN",

        # CLI
        "cli.description": "Markdown / mrkdwn → 精美 PDF 转换工具",
        "cli.epilog": textwrap.dedent("""\
            示例:
              md2pdf README.md -o README.pdf
              md2pdf doc.md -o doc.pdf --toc --cover --title "文档标题" --author "作者"
              cat note.md | md2pdf -o note.pdf --font-size 12pt
              md2pdf input.md -o output.pdf --debug > output.html
        """),

        # CLI arg descriptions
        "arg.input": "输入 .md 文件（缺省则从 stdin 读取）",
        "arg.output": "输出文件路径（缺省则与输入文件同名同目录）",
        "arg.html": "输出 HTML 文件（代替 PDF，默认与输入文件同名同目录）",
        "arg.css": "自定义 CSS 文件路径（覆盖默认样式）",
        "arg.toc": "生成目录",
        "arg.cover": "生成封面页",
        "arg.title": "文档标题（用于封面和 HTML title）",
        "arg.author": "作者（用于封面）",
        "arg.font_size": "基础字号，如 12pt",
        "arg.paper_size": "纸张大小，如 A4, Letter",
        "arg.margin": "页边距，如 2cm",
        "arg.debug": "输出中间 HTML 到 stdout（不生成 PDF）",
        "arg.lang": "界面与文档语言（如 zh-CN, en）",

        # Error messages
        "error.file_not_found": "ERROR: 文件不存在: {path}",
        "error.stdin_empty": "ERROR: 没有输入内容（stdin 为空）",
        "error.weasyprint_not_found": "ERROR: 找不到 weasyprint。安装: pip install weasyprint",
        "error.weasyprint_timeout": "ERROR: WeasyPrint 超时",
        "error.output_required": "ERROR: 从 stdin 读取时需要指定 -o 输出路径",
        "error.pdf_failed": "ERROR: PDF 生成失败",
        "error.pdf_failed_detail": "ERROR: PDF 生成失败: {error}",
        "error.weasyprint_stderr": "ERROR: WeasyPrint: {stderr}",

        # Warnings
        "warn.css_not_found": "WARN: CSS 文件不存在: {path}，使用默认样式",

        # Progress
        "progress.generating": "生成 PDF: {path} ...",
        "progress.generating_html": "生成 HTML: {path} ...",
        "progress.done": "DONE: {path} ({size:.1f} KB)",

        # TOC
        "toc.title": "目录 / Table of Contents",

        # Cover
        "cover.meta": "{date}",
        "cover.author": "{author}",

        # Date format (for strftime)
        "date_format": "%Y-%m-%d",

        # HTML
        "html.title_suffix": "",

        # Font config (CSS font-family values)
        "font.serif": '"Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "Georgia", "Times New Roman", serif',
        "font.sans_serif": '"Source Han Sans SC", "Noto Sans CJK SC", "Helvetica Neue", "Arial", sans-serif',
        "font.mono": '"SF Mono", "Menlo", "Monaco", "Consolas", "Liberation Mono", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", monospace',
        "font.page_number": '"Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", serif',

        # MCP
        "mcp.tool.convert.description": "将 Markdown 文本转换为 PDF，返回 base64 编码的文件内容",
        "mcp.tool.convert_file.description": "将 .md 文件转换为 .pdf 文件",
        "mcp.tool.convert.arg.markdown": "Markdown 文本内容",
        "mcp.tool.convert.arg.filename": "输出文件名（可选，默认 output.pdf）",
        "mcp.tool.convert.arg.lang": "文档语言（如 zh-CN, en）",
        "mcp.tool.convert_file.arg.input": "输入的 .md 文件路径",
        "mcp.tool.convert_file.arg.output": "输出的 .pdf 文件路径",
        "mcp.tool.convert_file.arg.toc": "是否生成目录",
        "mcp.tool.convert_file.arg.cover": "是否生成封面",
        "mcp.tool.convert_file.arg.title": "文档标题",
        "mcp.tool.convert_file.arg.author": "作者",
        "mcp.tool.convert_file.arg.lang": "文档语言（如 zh-CN, en）",
    },

    "en": {
        "code": "en",
        "name": "English",
        "html_lang": "en",

        # CLI
        "cli.description": "Markdown / mrkdwn → Beautiful PDF Converter",
        "cli.epilog": textwrap.dedent("""\
            Examples:
              md2pdf README.md -o README.pdf
              md2pdf doc.md -o doc.pdf --toc --cover --title "Document Title" --author "Author"
              cat note.md | md2pdf -o note.pdf --font-size 12pt
              md2pdf input.md -o output.pdf --debug > output.html
        """),

        # CLI arg descriptions
        "arg.input": "Input .md file (reads from stdin if omitted)",
        "arg.output": "Output file path (defaults to same dir as input)",
        "arg.html": "Output HTML file instead of PDF (defaults to same dir as input)",
        "arg.css": "Custom CSS file path (overrides default styles)",
        "arg.toc": "Generate table of contents",
        "arg.cover": "Generate cover page",
        "arg.title": "Document title (for cover and HTML title)",
        "arg.author": "Author (for cover page)",
        "arg.font_size": "Base font size, e.g. 12pt",
        "arg.paper_size": "Paper size, e.g. A4, Letter",
        "arg.margin": "Page margin, e.g. 2cm",
        "arg.debug": "Output intermediate HTML to stdout (no PDF)",
        "arg.lang": "Interface and document language (e.g. zh-CN, en)",

        # Error messages
        "error.file_not_found": "ERROR: File not found: {path}",
        "error.stdin_empty": "ERROR: No input content (stdin is empty)",
        "error.weasyprint_not_found": "ERROR: weasyprint not found. Install: pip install weasyprint",
        "error.weasyprint_timeout": "ERROR: WeasyPrint timed out",
        "error.output_required": "ERROR: -o is required when reading from stdin",
        "error.pdf_failed": "ERROR: PDF generation failed",
        "error.pdf_failed_detail": "ERROR: PDF generation failed: {error}",
        "error.weasyprint_stderr": "ERROR: WeasyPrint: {stderr}",

        # Warnings
        "warn.css_not_found": "WARN: CSS file not found: {path}, using default styles",

        # Progress
        "progress.generating": "Generating PDF: {path} ...",
        "progress.generating_html": "Generating HTML: {path} ...",
        "progress.done": "DONE: {path} ({size:.1f} KB)",

        # TOC
        "toc.title": "Table of Contents",

        # Cover
        "cover.meta": "{date}",
        "cover.author": "{author}",

        # Date format
        "date_format": "%B %d, %Y",

        # HTML
        "html.title_suffix": "",

        # Font config
        "font.serif": '"Georgia", "Times New Roman", serif',
        "font.sans_serif": '"Helvetica Neue", "Arial", sans-serif',
        "font.mono": '"SF Mono", "Menlo", "Monaco", "Consolas", "Liberation Mono", monospace',
        "font.page_number": '"Georgia", "Times New Roman", serif',

        # MCP
        "mcp.tool.convert.description": "Convert Markdown text to PDF, returns base64-encoded file",
        "mcp.tool.convert_file.description": "Convert .md file to .pdf file",
        "mcp.tool.convert.arg.markdown": "Markdown text content",
        "mcp.tool.convert.arg.filename": "Output filename (optional, default output.pdf)",
        "mcp.tool.convert.arg.lang": "Document language (e.g. zh-CN, en)",
        "mcp.tool.convert_file.arg.input": "Input .md file path",
        "mcp.tool.convert_file.arg.output": "Output .pdf file path",
        "mcp.tool.convert_file.arg.toc": "Generate table of contents",
        "mcp.tool.convert_file.arg.cover": "Generate cover page",
        "mcp.tool.convert_file.arg.title": "Document title",
        "mcp.tool.convert_file.arg.author": "Author",
        "mcp.tool.convert_file.arg.lang": "Document language (e.g. zh-CN, en)",
    },
}

# Language code normalization mapping (lowercase normalized -> canonical key)
SUPPORTED_LANGS = {
    "zh-cn": "zh-CN",
    "zh": "zh-CN",
    "zh_cn": "zh-CN",
    "en": "en",
    "en-us": "en",
    "en_us": "en",
}

DEFAULT_LANG = "zh-CN"


def resolve_lang(code: str) -> str:
    """Resolve a user-supplied language code to a canonical language key.

    Accepts flexible inputs like 'zh', 'zh-CN', 'zh_CN', 'en', 'en-US'.
    Falls back to DEFAULT_LANG for unsupported codes.
    """
    if not code:
        return DEFAULT_LANG
    normalized = code.lower().replace("-", "_")
    return SUPPORTED_LANGS.get(normalized, DEFAULT_LANG)


class Lang:
    """Language translation helper.

    Provides dictionary-like access to translated strings with
    optional format argument substitution.

    Usage:
        t = Lang("en")
        msg = t.get("error.file_not_found", path="README.md")
        # -> "ERROR: File not found: README.md"
    """

    def __init__(self, code: str = DEFAULT_LANG):
        self.code = resolve_lang(code)
        self._strings = LANGUAGES.get(self.code, LANGUAGES[DEFAULT_LANG])

    def __getitem__(self, key: str) -> str:
        """Get raw translated string by key."""
        value = self._strings.get(key)
        if value is not None:
            return value
        # Fall back to default language
        fallback = LANGUAGES[DEFAULT_LANG].get(key)
        if fallback is not None:
            return fallback
        return f"??{key}??"

    def get(self, key: str, **kwargs) -> str:
        """Get translated string and substitute format placeholders.

        Example:
            t.get("error.file_not_found", path="foo.md")
        """
        template = self[key]
        if kwargs:
            return template.format(**kwargs)
        return template

    def __contains__(self, key: str) -> bool:
        return key in self._strings


def lang_for(code: str = DEFAULT_LANG) -> Lang:
    """Convenience factory: create a Lang instance from a language code."""
    return Lang(code=code)
