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
        'language': post.metadata.get('language'),
        'repository': post.metadata.get('repository'),
        'category': post.metadata.get('label'),
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


def filter_reviewers(reviewers, language=None, repo=None, category=None):
    def match(value, expected):
        if not expected:
            return True
        if value is None:
            return False
        return str(value).lower() == str(expected).lower()

    results = []
    for r in reviewers:
        if not match(r.get('language'), language):
            continue
        if not match(r.get('repository'), repo):
            continue
        if not match(r.get('category'), category):
            continue
        results.append(r)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description='Awesome Reviewers CLI')
    sub = parser.add_subparsers(dest='command')
    add = sub.add_parser('add')
    add.add_argument('reviewers', nargs='*', help='reviewer names without extension')
    add.add_argument('--target', nargs='+', choices=list(writers.keys()), required=True)
    add.add_argument('--all', action='store_true', help='process all reviewers')
    add.add_argument('--language')
    add.add_argument('--repo')
    add.add_argument('--category')
    add.add_argument('--output-dir', default='.', help='output directory')

    ls = sub.add_parser('list')
    ls.add_argument('--language')
    ls.add_argument('--repo')
    ls.add_argument('--category')

    args = parser.parse_args(argv)

    if args.command == 'add':
        if args.all or args.language or args.repo or args.category:
            all_reviewers = load_all_reviewers()
            selected = filter_reviewers(all_reviewers, args.language, args.repo, args.category)
            for target in args.target:
                writer_cls = writers[target]
                subset = [r for r in selected if target in r.get('tools', [])]
                if subset:
                    writer_cls().write(subset, args.output_dir)
        else:
            if not args.reviewers:
                parser.error('reviewer name required if no filters specified')
            reviewers = load_reviewers(args.reviewers)
            for target in args.target:
                writer_cls = writers[target]
                writer_cls().write(reviewers, args.output_dir)
    elif args.command == 'list':
        reviewers = load_all_reviewers()
        reviewers = filter_reviewers(reviewers, args.language, args.repo, args.category)
        for r in reviewers:
            parts = [r.get('name')]
            if r.get('language'):
                parts.append(f"language={r['language']}")
            if r.get('repository'):
                parts.append(f"repo={r['repository']}")
            if r.get('category'):
                parts.append(f"category={r['category']}")
            print(' '.join(parts))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
