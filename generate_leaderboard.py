#!/usr/bin/env python3
"""Generate aggregated contributor leaderboard data."""
import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import yaml

from github_utils import fetch_profile

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
        'comments': defaultdict(list)
    })
    for json_path in reviewers_dir.glob('*.json'):
        slug = json_path.stem
        meta = parse_front_matter(reviewers_dir / f'{slug}.md')
        title = meta.get('title', slug)
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
                if author == 'Copilot':
                    continue
                info = users[author]
                info['reviewers'].add(slug)
                info['entry_titles'][slug] = title
                if repo:
                    info['repos'].add(repo)
                if text:
                    info['comments'][slug].append(text)
                dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
                if info['last'] is None or dt > info['last']:
                    info['last'] = dt

    human_output = []
    bot_output = []
    for user, d in users.items():
        entry = {
            'name': user,
            'reviewers_count': len(d['reviewers']),
            'repos_count': len(d['repos']),
            'last_contribution': d['last'].isoformat() if d['last'] else None
        }
        if '[bot]' in user:
            bot_output.append(entry)
        else:
            human_output.append(entry)

    human_output.sort(key=lambda x: x['reviewers_count'], reverse=True)
    bot_output.sort(key=lambda x: x['reviewers_count'], reverse=True)
    # Keep only the top 100 contributors in each list to keep the dataset small
    human_output = human_output[:100]
    bot_output = bot_output[:100]

    top_users = {u['name'] for u in human_output + bot_output}

    # Load existing contributor data to reuse cached profiles
    assets_dir = Path('assets/data')
    assets_dir.mkdir(parents=True, exist_ok=True)
    existing = {}
    existing_path = assets_dir / 'contributors.json'
    if existing_path.exists():
        try:
            with open(existing_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except Exception:
            existing = {}

    token = os.getenv('GITHUB_TOKEN')

    contributors = {}
    for user in top_users:
        d = users[user]
        entries = [
            {'slug': s, 'title': d['entry_titles'][s]}
            for s in sorted(d['entry_titles'])
        ]
        info = {
            'repos': sorted(d['repos']),
            'entries': entries,
            'comments': {k: v for k, v in d['comments'].items()}
        }
        profile = existing.get(user, {}).get('profile')
        if profile is None:
            profile = fetch_profile(user, token)
        if profile is not None:
            info['profile'] = profile
        contributors[user] = info

    data_dir = Path('_data')
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / 'leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(human_output, f, indent=2, ensure_ascii=False)
    with open(data_dir / 'ai_leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(bot_output, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(human_output)} contributors to _data/leaderboard.json')
    print(f'Wrote {len(bot_output)} contributors to _data/ai_leaderboard.json')

    with open(assets_dir / 'contributors.json', 'w', encoding='utf-8') as f:
        json.dump({u: contributors[u] for u in top_users if u in {x["name"] for x in human_output}}, f, indent=2, ensure_ascii=False)
    with open(assets_dir / 'ai_contributors.json', 'w', encoding='utf-8') as f:
        json.dump({u: contributors[u] for u in top_users if u in {x["name"] for x in bot_output}}, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(human_output)} users to assets/data/contributors.json')
    print(f'Wrote {len(bot_output)} users to assets/data/ai_contributors.json')

if __name__ == '__main__':
    main()
