"""核心功能测试：md_to_html 及其衍生方法。"""

import os
import tempfile
import unittest

from md2pdf import (
    md_to_html,
    md_to_html_file,
    convert_to_html,
    convert,
    Lang,
)


SAMPLE_MD = """\
# Hello World

This is a **markdown** document.

- Item 1
- Item 2

```python
print("hello")
```
"""

SAMPLE_MD_WITH_TOC = """\
# Title

## Section 1

Content here.

### Subsection 1.1

More content.

## Section 2

Final content.
"""


class TestMdToHtml(unittest.TestCase):
    """Test the core md_to_html() function."""

    def test_basic_conversion(self):
        """Basic Markdown → HTML conversion produces a complete document."""
        html = md_to_html(SAMPLE_MD)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<html lang=", html)
        self.assertIn("<h1>Hello World</h1>", html)
        self.assertIn("<strong>markdown</strong>", html)
        self.assertIn("</html>", html)

    def test_html_lang_zh_default(self):
        """Default language is zh-CN."""
        html = md_to_html(SAMPLE_MD)
        self.assertIn('lang="zh-CN"', html)

    def test_html_lang_en(self):
        """English language sets html lang=en."""
        html = md_to_html(SAMPLE_MD, lang="en")
        self.assertIn('lang="en"', html)

    def test_toc_generation(self):
        """--toc generates table of contents div."""
        html = md_to_html(SAMPLE_MD_WITH_TOC, toc=True)
        self.assertIn('<div class="toc">', html)
        self.assertIn("Table of Contents", html)

    def test_toc_title_chinese(self):
        """Chinese TOC title is '目录 / Table of Contents'."""
        html = md_to_html(SAMPLE_MD_WITH_TOC, toc=True, lang="zh-CN")
        self.assertIn("目录 / Table of Contents", html)

    def test_toc_title_english(self):
        """English TOC title is 'Table of Contents'."""
        html = md_to_html(SAMPLE_MD_WITH_TOC, toc=True, lang="en")
        self.assertIn("<h2>Table of Contents</h2>", html)

    def test_cover_generation(self):
        """--cover generates cover-page div."""
        html = md_to_html(SAMPLE_MD, cover=True, title="Test", author="Tester")
        self.assertIn('<div class="cover-page">', html)
        self.assertIn("<h1>Test</h1>", html)
        self.assertIn("Tester", html)

    def test_code_syntax_highlighting(self):
        """Code blocks get Pygments highlighting."""
        html = md_to_html(SAMPLE_MD)
        self.assertIn('class="codehilite', html)

    def test_custom_css(self):
        """Custom CSS is injected into the style tag."""
        custom = "body { color: red; }"
        html = md_to_html(SAMPLE_MD, css=custom)
        self.assertIn("body { color: red; }", html)

    def test_title_in_html(self):
        """Title appears in both <title> and <h1> (if cover)."""
        html = md_to_html(SAMPLE_MD, title="MyDoc")
        self.assertIn("<title>MyDoc</title>", html)


class TestMdToHtmlFile(unittest.TestCase):
    """Test md_to_html_file() — writing HTML to disk."""

    def test_write_html_file(self):
        """HTML is written to the specified file path."""
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        tmp.close()
        try:
            ok = md_to_html_file(SAMPLE_MD, tmp.name)
            self.assertTrue(ok)
            content = open(tmp.name, encoding="utf-8").read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("<h1>Hello World</h1>", content)
        finally:
            os.unlink(tmp.name)


class TestConvertToHtml(unittest.TestCase):
    """Test convert_to_html() — public alias for md_to_html()."""

    def test_returns_html_string(self):
        """Returns a complete HTML document string."""
        html = convert_to_html(SAMPLE_MD, lang="en")
        self.assertIsInstance(html, str)
        self.assertIn("<html lang=", html)


class TestConvertFunction(unittest.TestCase):
    """Test convert() with output_format='html'."""

    def test_convert_to_html_file(self):
        """convert() with output_format='html' writes an HTML file."""
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        tmp.close()
        try:
            ok = convert(SAMPLE_MD, tmp.name, output_format="html")
            self.assertTrue(ok)
            content = open(tmp.name, encoding="utf-8").read()
            self.assertIn("<!DOCTYPE html>", content)
        finally:
            os.unlink(tmp.name)


class TestI18n(unittest.TestCase):
    """Test the i18n / Lang helper."""

    def test_lang_zh_default(self):
        """Default language resolves to zh-CN."""
        t = Lang()
        self.assertEqual(t.code, "zh-CN")

    def test_lang_en(self):
        """English language resolves correctly."""
        t = Lang("en")
        self.assertEqual(t.code, "en")

    def test_lang_unstable_fallback(self):
        """Unknown language falls back to zh-CN."""
        t = Lang("fr")
        self.assertEqual(t.code, "zh-CN")

    def test_translation_lookup(self):
        """Translation keys return expected values."""
        t = Lang("en")
        self.assertIn("Beautiful PDF", t.get("cli.description"))
        t_zh = Lang("zh-CN")
        self.assertIn("精美 PDF", t_zh.get("cli.description"))

    def test_translation_with_format(self):
        """Translation with format arguments works."""
        t = Lang("en")
        msg = t.get("error.file_not_found", path="test.md")
        self.assertIn("test.md", msg)
        self.assertIn("File not found", msg)


if __name__ == "__main__":
    unittest.main()
