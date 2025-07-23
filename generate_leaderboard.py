#!/usr/bin/env python3
"""Generate aggregated contributor leaderboard data."""
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import yaml

def parse_front_matter(md_path):
    try:
        text = md_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return {}
    if not text.startswith('---'):
        return {}
    parts = text.split('---', 2)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1]) or {}
    return {}

def main():
    reviewers_dir = Path('_reviewers')
    users = defaultdict(lambda: {'reviewers': set(), 'repos': set(), 'categories': set(), 'last': None})
    for json_path in reviewers_dir.glob('*.json'):
        slug = json_path.stem
        meta = parse_front_matter(reviewers_dir / f'{slug}.md')
        label = meta.get('label')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            repo = item.get('repo_full_name')
            for c in item.get('discussion_comments', []):
                author = c.get('comment_author')
                ts = c.get('comment_created_at')
                if not author or not ts:
                    continue
                info = users[author]
                info['reviewers'].add(slug)
                if repo:
                    info['repos'].add(repo)
                if label:
                    info['categories'].add(label)
                dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
                if info['last'] is None or dt > info['last']:
                    info['last'] = dt

    output = []
    for user, d in users.items():
        output.append({
            'name': user,
            'reviewers_count': len(d['reviewers']),
            'repos_count': len(d['repos']),
            'last_contribution': d['last'].isoformat() if d['last'] else None,
            'categories': sorted(d['categories'])
        })
    output.sort(key=lambda x: x['reviewers_count'], reverse=True)
    # Keep only the top 100 contributors to keep the dataset small
    output = output[:100]

    data_dir = Path('_data')
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / 'leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(output)} contributors to _data/leaderboard.json')

if __name__ == '__main__':
    main()
