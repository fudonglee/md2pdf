import os
import sys
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from . import __version__
from .css import get_css
from .parser import parse_markdown
from .utils import (
    preprocess_strip_wrapping_fence,
    preprocess_mrkdwn,
    slugify,
    escape_html,
    today,
)
from .i18n import lang_for, DEFAULT_LANG


def _generate_toc(html: str, lang: str = DEFAULT_LANG) -> str:
    pattern = re.compile(r'<(h[1-4])\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
    entries = []
    for tag, content in pattern.findall(html):
        level = int(tag[1])
        text_only = re.sub(r'<[^>]+>', '', content).strip()
        anchor_id = f"toc-{slugify(text_only)}"
        entries.append((level, text_only, anchor_id))
    if not entries:
        return ""
    t = lang_for(lang)
    toc_title = t.get("toc.title")
    lines = ['<div class="toc">', f'<h2>{escape_html(toc_title)}</h2>']
    for level, text, anchor_id in entries:
        lines.append(f'<a class="toc-h{level}" href="#{anchor_id}">{escape_html(text)}</a>')
    lines.append("</div>")
    return "\n".join(lines)


def md_to_html(
    md_text: str,
    css: str = None,
    toc: bool = False,
    cover: bool = False,
    title: str = "",
    author: str = "",
    lang: str = DEFAULT_LANG,
) -> str:
    t = lang_for(lang)

    md_text = preprocess_strip_wrapping_fence(md_text)
    md_text = preprocess_mrkdwn(md_text)
    body_html = parse_markdown(md_text)

    toc_html = _generate_toc(body_html, lang) if toc else ""

    cover_html = ""
    if cover:
        date_str = datetime.now().strftime(t.get("date_format"))
        cover_html = f"""\
<div class="cover-page">
  <h1>{escape_html(title or '')}</h1>
  {f'<p class="meta">{escape_html(author)}</p>' if author else ''}
  <p class="meta">{escape_html(date_str)}</p>
</div>"""

    resolved_css = css if css is not None else get_css(lang)
    html_lang = t.get("html_lang")

    return f"""\
<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape_html(title or 'Document')}</title>
<style>
{resolved_css}
</style>
</head>
<body>
{cover_html}
{toc_html}
{body_html}
</body>
</html>"""


def _find_weasyprint() -> str | None:
    candidates = [
        "/opt/anaconda3/bin/weasyprint",
    ]
    import shutil
    wp = shutil.which("weasyprint")
    if wp:
        return wp
    for p in candidates:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    extra = [
        "/usr/local/bin/weasyprint",
        "/usr/bin/weasyprint",
        os.path.expanduser("~/.local/bin/weasyprint"),
    ]
    for p in extra:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def html_to_pdf(html: str, output_path: str) -> bool:
    tmp_html = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
    try:
        tmp_html.write(html)
        tmp_html.close()
        wp = _find_weasyprint()
        if not wp:
            t = lang_for()
            print(t.get("error.weasyprint_not_found"), file=sys.stderr)
            return False
        result = subprocess.run(
            [wp, tmp_html.name, output_path],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            t = lang_for()
            print(t.get("error.weasyprint_stderr", stderr=result.stderr.strip()), file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        t = lang_for()
        print(t.get("error.weasyprint_timeout"), file=sys.stderr)
        return False
    except Exception as e:
        t = lang_for()
        print(t.get("error.pdf_failed_detail", error=str(e)), file=sys.stderr)
        return False
    finally:
        os.unlink(tmp_html.name)


def convert(md_text: str, output_path: str, **kwargs) -> bool:
    """One-step conversion: Markdown -> HTML -> PDF."""
    html = md_to_html(md_text, **kwargs)
    return html_to_pdf(html, output_path)


def convert_file(input_path: str, output_path: str, **kwargs) -> bool:
    """Convert a .md file to .pdf, inferring title from filename."""
    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    title = kwargs.pop("title", None) or Path(input_path).stem
    return convert(md_text, output_path, title=title, **kwargs)
