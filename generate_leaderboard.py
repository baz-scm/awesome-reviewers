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
    users = defaultdict(lambda: {
        'reviewers': set(),
        'repos': set(),
        'last': None,
        'entry_titles': {},
        'comments': defaultdict(list),
        'labels': defaultdict(int),
    })
    label_map = {}
    for json_path in reviewers_dir.glob('*.json'):
        slug = json_path.stem
        meta = parse_front_matter(reviewers_dir / f'{slug}.md')
        title = meta.get('title', slug)
        label = meta.get('label')
        if label:
            label_map[slug] = label
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            repo = item.get('repo_full_name')
            for c in item.get('discussion_comments', []):
                author = c.get('comment_author')
                ts = c.get('comment_created_at')
                text = c.get('comment_body')
                if not author or not ts:
                    continue
                if author == 'Copilot' or '[bot]' in author:
                    continue
                info = users[author]
                info['reviewers'].add(slug)
                info['entry_titles'][slug] = title
                if label:
                    info['labels'][label] += 1
                if repo:
                    info['repos'].add(repo)
                if text:
                    info['comments'][slug].append(text)
                dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
                if info['last'] is None or dt > info['last']:
                    info['last'] = dt

    output = []
    for user, d in users.items():
        output.append({
            'name': user,
            'reviewers_count': len(d['reviewers']),
            'repos_count': len(d['repos']),
            'last_contribution': d['last'].isoformat() if d['last'] else None
        })
    output.sort(key=lambda x: x['reviewers_count'], reverse=True)
    # Keep only the top 100 contributors to keep the dataset small
    output = output[:100]

    top_users = {u['name'] for u in output}

    contributors = {}
    for user in top_users:
        d = users[user]
        entries = [
            {'slug': s, 'title': d['entry_titles'][s]}
            for s in sorted(d['entry_titles'])
        ]
        label_counts = sorted(d['labels'].items(), key=lambda x: (-x[1], x[0]))
        top_labels = [l for l, _ in label_counts[:3]]
        contributors[user] = {
            'repos': sorted(d['repos']),
            'entries': entries,
            'comments': {k: v for k, v in d['comments'].items()},
            'labels': top_labels,
        }

    data_dir = Path('_data')
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / 'leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(output)} contributors to _data/leaderboard.json')

    assets_dir = Path('assets/data')
    assets_dir.mkdir(parents=True, exist_ok=True)
    with open(assets_dir / 'contributors.json', 'w', encoding='utf-8') as f:
        json.dump(contributors, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(contributors)} users to assets/data/contributors.json')

    with open(assets_dir / 'reviewer_labels.json', 'w', encoding='utf-8') as f:
        json.dump(label_map, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(label_map)} labels to assets/data/reviewer_labels.json')

if __name__ == '__main__':
    main()
