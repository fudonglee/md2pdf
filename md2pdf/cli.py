import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .renderer import md_to_html, html_to_pdf
from .i18n import lang_for, resolve_lang, DEFAULT_LANG


def build_parser(lang_code: str = DEFAULT_LANG):
    t = lang_for(lang_code)
    p = argparse.ArgumentParser(
        prog="md2pdf",
        description=t.get("cli.description"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=t.get("cli.epilog"),
    )
    p.add_argument("input", nargs="?", help=t.get("arg.input"))
    p.add_argument("-o", "--output", help=t.get("arg.output"))
    p.add_argument("--html", action="store_true", help=t.get("arg.html"))
    p.add_argument("--css", help=t.get("arg.css"))
    p.add_argument("--toc", action="store_true", help=t.get("arg.toc"))
    p.add_argument("--cover", action="store_true", help=t.get("arg.cover"))
    p.add_argument("--title", default="", help=t.get("arg.title"))
    p.add_argument("--author", default="", help=t.get("arg.author"))
    p.add_argument("--font-size", default="", help=t.get("arg.font_size"))
    p.add_argument("--paper-size", default="A4", help=t.get("arg.paper_size"))
    p.add_argument("--margin", default="2.5cm 2cm", help=t.get("arg.margin"))
    p.add_argument("--debug", action="store_true", help=t.get("arg.debug"))
    p.add_argument("--lang", default=DEFAULT_LANG, help=t.get("arg.lang"))
    p.add_argument("--version", action="version", version=f"md2pdf {__version__}")
    return p


def _detect_lang_from_argv() -> str:
    for i, arg in enumerate(sys.argv):
        if arg == "--lang" and i + 1 < len(sys.argv):
            return resolve_lang(sys.argv[i + 1])
        if arg.startswith("--lang="):
            return resolve_lang(arg.split("=", 1)[1])
    return DEFAULT_LANG


def _resolve_output_path(input_path, html_mode):
    """Derive default output path from input file path.

    Rule: output goes to the SAME directory as the input file,
    with the same stem but different extension (.pdf or .html).
    """
    ext = ".html" if html_mode else ".pdf"
    return str(input_path.with_suffix(ext))


def main():
    lang_code = _detect_lang_from_argv()
    t = lang_for(lang_code)

    parser = build_parser(lang_code)
    args = parser.parse_args()

    if args.lang:
        lang_code = resolve_lang(args.lang)
        t = lang_for(lang_code)

    html_mode = args.html

    # --- Read input ---
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(t.get("error.file_not_found", path=args.input), file=sys.stderr)
            sys.exit(1)
        md_text = input_path.read_text(encoding="utf-8")
        auto_title = input_path.stem
        # Default output path = same dir as input
        if not args.output:
            args.output = _resolve_output_path(input_path, html_mode)
    else:
        # Reading from stdin
        md_text = sys.stdin.read()
        if not md_text.strip():
            print(t.get("error.stdin_empty"), file=sys.stderr)
            sys.exit(1)
        auto_title = "Document"
        if not args.output:
            print(t.get("error.output_required"), file=sys.stderr)
            sys.exit(1)

    # --- CSS ---
    css_content = None
    if args.css:
        css_path = Path(args.css)
        if css_path.exists():
            css_content = css_path.read_text(encoding="utf-8")
        else:
            print(t.get("warn.css_not_found", path=args.css), file=sys.stderr)

    # --- Generate HTML ---
    html = md_to_html(
        md_text=md_text,
        css=css_content,
        toc=args.toc,
        cover=args.cover,
        title=args.title or auto_title,
        author=args.author,
        lang=lang_code,
    )

    # --- Output ---
    if args.debug:
        print(html)
        return

    output_path = args.output

    if html_mode:
        # Write HTML file directly
        print(t.get("progress.generating_html", path=output_path), file=sys.stderr)
        try:
            Path(output_path).write_text(html, encoding="utf-8")
            size_kb = os.path.getsize(output_path) / 1024
            print(t.get("progress.done", path=output_path, size=size_kb), file=sys.stderr)
        except OSError as e:
            print(t.get("error.pdf_failed_detail", error=str(e)), file=sys.stderr)
            sys.exit(1)
    else:
        # Generate PDF (existing behavior)
        print(t.get("progress.generating", path=output_path), file=sys.stderr)
        success = html_to_pdf(html, output_path)
        if success:
            size_kb = os.path.getsize(output_path) / 1024
            print(t.get("progress.done", path=output_path, size=size_kb), file=sys.stderr)
        else:
            print(t.get("error.pdf_failed"), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
