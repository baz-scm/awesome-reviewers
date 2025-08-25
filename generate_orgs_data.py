#!/usr/bin/env python3
"""Generate organization-level data for reviewers."""
import json
from pathlib import Path
from datetime import datetime

REVIEWERS_DIR = Path('_reviewers')
CONTRIBUTORS_PATH = Path('assets/data/contributors.json')
OUTPUT_PATH = Path('_data/orgs.json')


def get_reviewer_info(slug: str) -> dict | None:
    """Return basic info about a reviewer entry.

    Extracts repository, title and comments count from the markdown front matter
    and uses the associated JSON discussion file to find the last contribution
    timestamp.
    """
    md_path = REVIEWERS_DIR / f'{slug}.md'
    if not md_path.exists():
        return None
    info: dict[str, str] = {}
    with md_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines or lines[0].strip() != '---':
        return None
    for line in lines[1:]:
        line = line.strip()
        if line == '---':
            break
        if ':' in line:
            key, val = line.split(':', 1)
            info[key.strip()] = val.strip()
    repo = info.get('repository')
    title = info.get('title')
    comments = int(info.get('comments_count', '0'))

    # find most recent comment timestamp
    json_path = REVIEWERS_DIR / f'{slug}.json'
    last_contrib = None
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
            for item in data:
                ts = item.get('created_at')
                if ts and (not last_contrib or ts > last_contrib):
                    last_contrib = ts
        except Exception:
            pass
    return {
        'repo': repo,
        'title': title,
        'comments_count': comments,
        'last_contribution': last_contrib,
    }


def main() -> None:
    data = json.loads(CONTRIBUTORS_PATH.read_text(encoding='utf-8'))
    orgs: dict[str, dict] = {}
    contributors: dict[str, dict] = {}

    for user, info in data.items():
        contrib = contributors.setdefault(user, {
            'reviewers_count': 0,
            'repos': set(),
            'last_contribution': None,
        })
        for entry in info.get('entries', []):
            slug = entry.get('slug')
            if not slug:
                continue
            rinfo = get_reviewer_info(slug)
            if not rinfo or not rinfo['repo']:
                continue
            repo = rinfo['repo']
            owner = repo.split('/')[0]
            org = orgs.setdefault(owner, {
                'contributors': set(),
                'reviewers_count': 0,
                'repos': set(),
                'reviews': []
            })
            org['contributors'].add(user)
            org['reviewers_count'] += 1
            org['repos'].add(repo)
            org['reviews'].append({
                'slug': slug,
                'title': rinfo['title'],
                'repo': repo,
                'comments': rinfo['comments_count']
            })

            contrib['reviewers_count'] += 1
            contrib['repos'].add(repo)
            lc = rinfo['last_contribution']
            if lc and (not contrib['last_contribution'] or lc > contrib['last_contribution']):
                contrib['last_contribution'] = lc

    output = {
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'orgs': []
    }
    for name, info in orgs.items():
        contributors_list = []
        for username in sorted(info['contributors']):
            stats = contributors.get(username, {})
            contributors_list.append({
                'name': username,
                'reviewers_count': stats.get('reviewers_count', 0),
                'repos_count': len(stats.get('repos', [])),
                'last_contribution': stats.get('last_contribution')
            })
        output['orgs'].append({
            'name': name,
            'reviewers_count': info['reviewers_count'],
            'repos_count': len(info['repos']),
            'contributors': contributors_list,
            'reviews': info['reviews']
        })
    output['orgs'].sort(key=lambda x: x['reviewers_count'], reverse=True)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(f"Wrote {len(output['orgs'])} orgs to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
