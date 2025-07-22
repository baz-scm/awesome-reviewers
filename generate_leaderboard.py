import json, os
from collections import defaultdict

reviewers_dir = '_reviewers'
contributors = defaultdict(lambda: {'entries': set(), 'repos': set()})

for fname in os.listdir(reviewers_dir):
    if not fname.endswith('.json'): continue
    path = os.path.join(reviewers_dir, fname)
    with open(path) as f:
        data = json.load(f)
    slug = fname[:-5]
    for discussion in data:
        comments = discussion.get('discussion_comments')
        if not comments:
            continue
        for comment in comments:
            user = comment.get('comment_author')
            if not user or '[bot]' in user:
                continue
            repo = comment.get('repo_full_name')
            contributors[user]['entries'].add(slug)
            if repo:
                contributors[user]['repos'].add(repo)

leaderboard = []
for user, info in contributors.items():
    leaderboard.append({
        'user': user,
        'entries_count': len(info['entries']),
        'repos_count': len(info['repos']),
        'repos': sorted(info['repos'])
    })

leaderboard.sort(key=lambda x: -x['entries_count'])
leaderboard = leaderboard[:50]

with open(os.path.join('_data','leaderboard.json'), 'w') as f:
    json.dump(leaderboard, f, indent=2)
