#!/usr/bin/env python3
import os
import glob
import yaml
import urllib.parse

REVIEWER_DIR = '_reviewers'
SITE_URL = 'https://awesomereviewers.com'

slugs = []
repos = set()
labels = set()
languages = set()

for path in sorted(glob.glob(os.path.join(REVIEWER_DIR, '*.md'))):
    slug = os.path.splitext(os.path.basename(path))[0]
    slugs.append(slug)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1]) or {}
            repo = front_matter.get('repository')
            label = front_matter.get('label')
            language = front_matter.get('language')
            if repo:
                repos.add(str(repo))
            if label:
                labels.add(str(label))
            if language:
                languages.add(str(language))

def write_robots(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('User-agent: *\n')
        f.write('Disallow:\n\n')
        f.write('Sitemap: https://awesomereviewers.com/sitemap.xml\n\n')
        for slug in slugs:
            f.write(f'Allow: /reviewers/{slug}/\n')
        for repo in sorted(repos):
            f.write(f'Allow: /?repos={urllib.parse.quote(repo)}\n')
        for label in sorted(labels):
            f.write(f'Allow: /?categories={urllib.parse.quote(label)}\n')
        for lang in sorted(languages):
            f.write(f'Allow: /?languages={urllib.parse.quote(lang)}\n')

def write_llms(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('## Reviewer Cards\n')
        for slug in slugs:
            f.write(f'- [{slug}]({SITE_URL}/reviewers/{slug}/)\n')
        f.write('\n## Filter Examples\n')
        for repo in sorted(repos):
            f.write(f'- {SITE_URL}/?repos={urllib.parse.quote(repo)}\n')
        for label in sorted(labels):
            f.write(f'- {SITE_URL}/?categories={urllib.parse.quote(label)}\n')
        for lang in sorted(languages):
            f.write(f'- {SITE_URL}/?languages={urllib.parse.quote(lang)}\n')

if __name__ == '__main__':
    write_robots('robots.txt')
    write_llms('llms.txt')
