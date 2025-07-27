#!/usr/bin/env python3
"""Interactively bundle multiple reviewer prompts into a single AGENTS.md file."""

from pathlib import Path
import yaml

REVIEWERS_DIR = Path('_reviewers')
OUTPUT_FILE = Path('AGENTS.md')


def parse_front_matter(md_path: Path):
    """Return metadata dict and markdown content without YAML front matter."""
    text = md_path.read_text(encoding='utf-8')
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            content = parts[2].lstrip()
            return meta, content
    return {}, text


def create_section(meta: dict, content: str) -> str:
    title = meta.get('title', 'Untitled')
    description = meta.get('description')
    section_lines = [f"## {title}"]
    if description:
        section_lines.append(description)
    section_lines.append('')
    section_lines.append(content.strip())
    section_lines.append('')
    return '\n'.join(section_lines)


def main():
    cart = []
    print("Enter reviewer slugs to add to your cart. Type 'checkout' to finish.")
    while True:
        choice = input('> ').strip()
        if not choice:
            continue
        if choice.lower() in {'checkout', 'exit'}:
            break
        path = REVIEWERS_DIR / f'{choice}.md'
        if path.exists():
            cart.append(choice)
            print(f"Added '{choice}' to cart.")
        else:
            print(f"Reviewer '{choice}' not found.")

    if not cart:
        print('No reviewers selected. Exiting.')
        return

    sections = []
    for slug in cart:
        meta, content = parse_front_matter(REVIEWERS_DIR / f'{slug}.md')
        sections.append(create_section(meta, content))

    output = '# Bundled Reviewers\n\n' + '\n'.join(sections)
    OUTPUT_FILE.write_text(output, encoding='utf-8')
    print(f'Wrote {len(cart)} reviewers to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
