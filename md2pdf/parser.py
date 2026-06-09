import re

from markdown_it import MarkdownIt
from mdit_py_plugins import (
    admon, amsmath, attrs, colon_fence, container,
    deflist, dollarmath, field_list, footnote,
    front_matter, myst_blocks, subscript, tasklists, texmath,
)

# Plugin function references
_front_matter_plugin = front_matter.front_matter_plugin
_footnote_plugin = footnote.footnote_plugin
_deflist_plugin = deflist.deflist_plugin
_tasklists_plugin = tasklists.tasklists_plugin
_sub_plugin = subscript.sub_plugin
_container_plugin = container.container_plugin
_admon_plugin = admon.admon_plugin
_colon_fence_plugin = colon_fence.colon_fence_plugin
_attrs_plugin = attrs.attrs_plugin

HAS_PYGMENTS = False
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    pass


def _code_highlight(code: str, lang: str = ""):
    if not HAS_PYGMENTS or not lang:
        escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code class="language-{lang}">{escaped}</code></pre>'
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except Exception:
        try:
            lexer = guess_lexer(code)
        except Exception:
            lexer = get_lexer_by_name("text")
    formatter = HtmlFormatter(nowrap=False, style="friendly")
    highlighted = highlight(code, lexer, formatter)
    return f'<div class="codehilite language-{lang}">{highlighted}</div>'


def make_parser():
    """构造 markdown-it 解析器，启用 GFM + 扩展特性。"""
    md = (
        MarkdownIt("commonmark", {"html": True, "breaks": False, "langPrefix": "language-"})
        .enable("table")
        .enable("strikethrough")
    )
    md.use(_front_matter_plugin)
    md.use(_footnote_plugin)
    md.use(_deflist_plugin)
    md.use(_tasklists_plugin)
    md.use(_sub_plugin)
    md.use(_container_plugin, name="info")
    md.use(_admon_plugin)
    md.use(_colon_fence_plugin)
    md.use(_attrs_plugin)

    def fence_highlight(self, tokens, idx, options, env):
        token = tokens[idx]
        info = token.info.strip()
        parts = info.split()
        lang = parts[0] if parts else ""
        return _code_highlight(token.content, lang)

    def code_block_render(self, tokens, idx, options, env):
        token = tokens[idx]
        return _code_highlight(token.content, "")

    md.add_render_rule("fence", fence_highlight)
    md.add_render_rule("code_block", code_block_render)

    return md


def parse_markdown(md_text: str) -> str:
    """将 Markdown 文本解析为 HTML 字符串。"""
    parser = make_parser()
    return parser.render(md_text)
