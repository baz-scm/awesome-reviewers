#!/usr/bin/env python3
"""Generate organization-level data for reviewers."""
import json
from pathlib import Path
from datetime import datetime

REVIEWERS_DIR = Path('_reviewers')
CONTRIBUTORS_PATH = Path('assets/data/contributors.json')
OUTPUT_PATH = Path('_data/orgs.json')


def get_repository(slug: str) -> str | None:
    md_path = REVIEWERS_DIR / f'{slug}.md'
    if not md_path.exists():
        return None
    with md_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines or lines[0].strip() != '---':
        return None
    for line in lines[1:]:
        line = line.strip()
        if line == '---':
            break
        if line.startswith('repository:'):
            return line.split(':', 1)[1].strip()
    return None


def main() -> None:
    data = json.loads(CONTRIBUTORS_PATH.read_text(encoding='utf-8'))
    orgs: dict[str, dict[str, set]] = {}
    for user, info in data.items():
        for entry in info.get('entries', []):
            slug = entry.get('slug')
            if not slug:
                continue
            repo = get_repository(slug)
            if not repo:
                continue
            owner = repo.split('/')[0]
            org = orgs.setdefault(owner, {'contributors': set(), 'reviewers_count': 0, 'repos': set()})
            org['contributors'].add(user)
            org['reviewers_count'] += 1
            org['repos'].add(repo)
    output = {
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'orgs': []
    }
    for name, info in orgs.items():
        output['orgs'].append({
            'name': name,
            'reviewers_count': info['reviewers_count'],
            'repos_count': len(info['repos']),
            'contributors': sorted(info['contributors'])
        })
    output['orgs'].sort(key=lambda x: x['reviewers_count'], reverse=True)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(f"Wrote {len(output['orgs'])} orgs to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
