#!/usr/bin/env python3
"""
Script to protect reviewer markdown bodies from Liquid processing.

Reviewer files are plain content: the code snippets and prose they contain
frequently include `{{ ... }}` or `{% ... %}` sequences (Go templates, GitHub
Actions expressions, Prometheus/JS object literals, ...). Jekyll parses those
as Liquid, which either silently swallows them or fails the whole build with a
Liquid syntax error.

For every file whose body contains Liquid-looking markers, the body is wrapped
in a single `{% raw %}` ... `{% endraw %}` block. The script is idempotent, so
CI can run it and fail if it produces changes.
"""

import re
import sys
from pathlib import Path

REVIEWERS_DIR = Path("_reviewers")

LIQUID_MARKER = re.compile(r"\{\{|\{%")
RAW_TAG_LINE = re.compile(r"^[ \t]*\{%-?\s*(?:raw|endraw)\s*-?%\}[ \t]*\n?", re.MULTILINE)
RAW_TAG_INLINE = re.compile(r"\{%-?\s*(?:raw|endraw)\s*-?%\}")


def split_front_matter(content):
    """Return (front_matter, body). front_matter includes the closing '---\\n'."""
    if not content.startswith("---"):
        return "", content

    match = re.match(r"^---\r?\n.*?\r?\n---[ \t]*\r?\n", content, re.DOTALL)
    if not match:
        return "", content

    return match.group(0), content[match.end():]


def escape_body(body):
    """Wrap a body in a single raw block, dropping any pre-existing raw tags."""
    stripped = RAW_TAG_LINE.sub("", body)
    stripped = RAW_TAG_INLINE.sub("", stripped)
    stripped = stripped.strip("\n")

    if not stripped:
        return body

    return "{% raw %}\n" + stripped + "\n{% endraw %}\n"


def process_file(filepath):
    """Escape one reviewer file. Returns True when the file was changed."""
    content = filepath.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(content)

    if not LIQUID_MARKER.search(body):
        return False

    new_content = front_matter + escape_body(body)
    if new_content == content:
        return False

    filepath.write_text(new_content, encoding="utf-8")
    return True


def main():
    if not REVIEWERS_DIR.exists():
        print(f"Error: {REVIEWERS_DIR} directory not found")
        return 1

    changed = []
    for filepath in sorted(REVIEWERS_DIR.glob("*.md")):
        if process_file(filepath):
            changed.append(filepath)
            print(f"  ✓ Escaped Liquid in {filepath}")

    print(f"\nEscaped {len(changed)} of {len(list(REVIEWERS_DIR.glob('*.md')))} reviewer files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
