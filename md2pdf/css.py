"""印刷级 CSS 样式模板，支持多语言字体适配。

CSS template uses $var syntax (string.Template) to avoid
conflict with CSS curly braces { } when substituting language-specific
font stacks.
"""

import string

# CSS template with $font_* placeholders for language-specific font stacks.
# Uses $var syntax (string.Template) to avoid conflict with CSS { } braces.
_PDF_CSS_SOURCE = r"""
@page {
  size: A4;
  margin: 2.5cm 2cm 2.5cm 2cm;
  @bottom-center {
    content: counter(page);
    font-family: $font_page;
    font-size: 9pt;
    color: #888;
  }
}

@page :first {
  @bottom-center { content: none; }
}

* { box-sizing: border-box; }

html {
  font-family: $font_serif;
  font-size: 11pt;
  line-height: 1.75;
  color: #1a1a1a;
  orphans: 3;
  widows: 3;
}

body { max-width: 100%; padding: 0; }

/* ---- 封面 ---- */
.cover-page {
  page-break-after: always;
  text-align: center;
  padding-top: 30vh;
}
.cover-page h1 {
  font-size: 28pt;
  font-weight: 700;
  color: #111;
  margin-bottom: 0.5em;
  letter-spacing: 0.05em;
}
.cover-page .subtitle { font-size: 14pt; color: #555; margin-bottom: 2em; }
.cover-page .meta { font-size: 10pt; color: #999; }

/* ---- 目录 ---- */
.toc { page-break-after: always; }
.toc h2 { font-size: 18pt; margin-bottom: 1em; border-bottom: 2px solid #333; padding-bottom: 0.3em; }
.toc a { color: #1a1a1a; text-decoration: none; display: block; padding: 0.2em 0; border-bottom: 1px dotted #ddd; }
.toc a:hover { color: #c00; }
.toc .toc-h1 { font-weight: 700; font-size: 11pt; }
.toc .toc-h2 { padding-left: 1.5em; font-size: 10.5pt; }
.toc .toc-h3 { padding-left: 3em; font-size: 10pt; color: #555; }
.toc .toc-h4 { padding-left: 4.5em; font-size: 9.5pt; color: #777; }

/* ---- 标题 ---- */
h1, h2, h3, h4, h5, h6 {
  font-family: $font_sans;
  font-weight: 700;
  color: #111;
  page-break-after: avoid;
  page-break-inside: avoid;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}
h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 0.3em; }
h2 { font-size: 16pt; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
h3 { font-size: 13pt; }
h4 { font-size: 11pt; font-style: italic; }

/* ---- 段落 ---- */
p { margin: 0.5em 0; text-align: justify; text-justify: inter-ideograph; }

/* ---- 链接 ---- */
a { color: #1a5276; text-decoration: underline; }
a:visited { color: #6c3483; }

/* ---- 强调 ---- */
strong, b { font-weight: 700; }
em, i { font-style: italic; }
s, del { text-decoration: line-through; }
u { text-decoration: underline; }
sup { font-size: 0.75em; vertical-align: super; }
sub { font-size: 0.75em; vertical-align: sub; }

/* ---- 引用 ---- */
blockquote {
  margin: 1em 0;
  padding: 0.5em 1em 0.5em 1.5em;
  border-left: 4px solid #2c3e50;
  background: #f8f9fa;
  color: #2c3e50;
  font-style: italic;
  page-break-inside: avoid;
}
blockquote p { margin: 0.3em 0; }

/* ---- 列表 ---- */
ul, ol { margin: 0.5em 0; padding-left: 2em; }
li { margin: 0.2em 0; }
li > p { margin: 0.2em 0; }

/* ---- 任务列表 ---- */
.task-list-item { list-style: none; margin-left: -1.5em; }
.task-list-item input[type="checkbox"] { margin-right: 0.5em; transform: scale(1.1); }
.task-list-item.checked { color: #666; }
.task-list-item.checked input[type="checkbox"] { accent-color: #27ae60; }

/* ---- 定义列表 ---- */
dl { margin: 0.8em 0; }
dt { font-weight: 700; margin-top: 0.5em; color: #2c3e50; }
dd { margin-left: 1.5em; color: #333; }

/* ---- 表格 ---- */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 9.5pt;
  page-break-inside: auto;
}
th, td {
  border: 1px solid #bbb;
  padding: 6px 10px;
  text-align: left;
  vertical-align: top;
}
th { background: #2c3e50; color: #fff; font-weight: 600; }
tr:nth-child(even) td { background: #f4f6f7; }

/* ---- 代码 ---- */
code {
  font-family: $font_mono;
  font-size: 0.85em;
  background: #f0f0f0;
  padding: 0.15em 0.4em;
  border-radius: 3px;
  color: #c0392b;
}
pre {
  font-family: $font_mono;
  font-size: 8.5pt;
  line-height: 1.6;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 0.8em 1em;
  margin: 0.8em 0;
  overflow-x: auto;
  page-break-inside: avoid;
  white-space: pre-wrap;
  word-break: break-all;
}
pre code { background: none; padding: 0; color: inherit; font-size: inherit; border-radius: 0; }

.codehilite {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 0.8em 1em;
  margin: 0.8em 0;
  overflow-x: auto;
  page-break-inside: avoid;
  font-size: 8.5pt;
  line-height: 1.5;
}
.codehilite pre, .codehilite code {
  font-family: $font_mono;
  background: none; border: none; padding: 0; margin: 0; font-size: inherit; color: inherit;
}

/* ---- 脚注 ---- */
.footnotes { margin-top: 2em; padding-top: 1em; border-top: 1px solid #ccc; font-size: 9pt; color: #555; }
.footnotes ol { padding-left: 1.5em; }
.footnotes li { margin: 0.3em 0; }
.footnote-backref { font-size: 0.8em; }

/* ---- 分割线 ---- */
hr { border: none; border-top: 2px solid #ccc; margin: 2em 0; page-break-after: avoid; }

/* ---- 图片 ---- */
img { max-width: 100%; height: auto; display: block; margin: 1em auto; page-break-inside: avoid; }

/* ---- mrkdwn Slack 风格 ---- */
.mrkdwn-mention { background: #e8f0fe; color: #1a73e8; padding: 0.1em 0.3em; border-radius: 3px; font-family: sans-serif; font-size: 0.9em; }
.mrkdwn-emoji { font-size: 1.2em; }

@media print {
  a { text-decoration: underline; color: #1a1a1a; }
  img { max-width: 100% !important; }
  pre, code { background: #f5f5f5 !important; }
}
"""

PDF_CSS_TEMPLATE = string.Template(_PDF_CSS_SOURCE)


def get_css(lang: str = "zh-CN") -> str:
    """Return CSS with language-appropriate font stacks."""
    from .i18n import lang_for
    t = lang_for(lang)
    return PDF_CSS_TEMPLATE.safe_substitute(
        font_serif=t.get("font.serif"),
        font_sans=t.get("font.sans_serif"),
        font_mono=t.get("font.mono"),
        font_page=t.get("font.page_number"),
    )
