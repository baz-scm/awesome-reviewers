#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import frontmatter
from writers import writers
import re

SECTION_RE = re.compile(r'^##\s*(.+)$', re.MULTILINE)


def parse_markdown(path: Path):
    post = frontmatter.load(path)
    content = post.content
    sections = {}
    current = None
    lines = []
    for line in content.splitlines():
        m = SECTION_RE.match(line)
        if m:
            if current:
                sections[current.lower()] = '\n'.join(lines).strip()
            current = m.group(1)
            lines = []
        else:
            if current is not None:
                lines.append(line)
    if current:
        sections[current.lower()] = '\n'.join(lines).strip()
    data = {
        'title': post.metadata.get('title', path.stem),
        'description': post.metadata.get('description'),
        'tools': post.metadata.get('tools', []),
        'system_prompt': sections.get('system prompt'),
        'goals': sections.get('goals'),
        'labels': sections.get('labels'),
    }
    return data


def load_reviewers(names, warn=True):
    reviewers = []
    for name in names:
        path = Path('_reviewers') / f'{name}.md'
        if not path.exists():
            if warn:
                print(f'Warning: reviewer {name} not found', file=sys.stderr)
            continue
        info = parse_markdown(path)
        if not info.get('system_prompt'):
            if warn:
                print(f'Warning: reviewer {name} missing ## System Prompt', file=sys.stderr)
            continue
        reviewers.append(info)
    return reviewers


def load_all_reviewers():
    reviewers = []
    for path in Path('_reviewers').glob('*.md'):
        info = parse_markdown(path)
        info['name'] = path.stem
        reviewers.append(info)
    return reviewers


def main(argv=None):
    parser = argparse.ArgumentParser(description='Awesome Reviewers CLI')
    sub = parser.add_subparsers(dest='command')
    add = sub.add_parser('add')
    add.add_argument('reviewers', nargs='*', help='reviewer names without extension')
    add.add_argument('--target', nargs='+', choices=list(writers.keys()), required=True)
    add.add_argument('--all', action='store_true', help='process all reviewers')
    add.add_argument('--output-dir', default='.', help='output directory')

    args = parser.parse_args(argv)

    if args.command == 'add':
        if args.all:
            all_reviewers = load_all_reviewers()
            for target in args.target:
                writer_cls = writers[target]
                selected = [r for r in all_reviewers if target in r.get('tools', [])]
                if selected:
                    writer_cls().write(selected, args.output_dir)
        else:
            if not args.reviewers:
                parser.error('reviewer name required if --all not specified')
            reviewers = load_reviewers(args.reviewers)
            for target in args.target:
                writer_cls = writers[target]
                writer_cls().write(reviewers, args.output_dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
