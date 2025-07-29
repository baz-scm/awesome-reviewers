import os
import glob
import yaml
from urllib.parse import quote


def parse_front_matter(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1])


def collect_data():
    reviewers = []
    repos = set()
    categories = set()
    languages = set()
    for md_file in glob.glob(os.path.join('_reviewers', '*.md')):
        slug = os.path.splitext(os.path.basename(md_file))[0]
        reviewers.append(slug)
        meta = parse_front_matter(md_file)
        repo = meta.get('repository')
        if repo:
            repos.add(str(repo))
        label = meta.get('label')
        if label:
            categories.add(str(label))
        language = meta.get('language')
        if language:
            languages.add(str(language))
    reviewers.sort()
    repos = sorted(repos)
    categories = sorted(categories)
    languages = sorted(languages)
    return reviewers, repos, categories, languages


def write_robots(reviewers, repos, categories, languages):
    lines = [
        'User-agent: *',
        'Disallow:',
        'Sitemap: https://awesomereviewers.com/sitemap.xml',
    ]
    lines += [f'Allow: /#{slug}' for slug in reviewers]
    lines += [f'Allow: /?repos={quote(r, safe="")}' for r in repos]
    lines += [f'Allow: /?categories={quote(c, safe="")}' for c in categories]
    lines += [f'Allow: /?languages={quote(l, safe="")}' for l in languages]
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def write_llms(reviewers, repos, categories, languages):
    lines = ['## Reviewer Cards']
    lines += [f'- [{slug}](https://awesomereviewers.com/#{slug})' for slug in reviewers]
    lines.append('')
    lines.append('## Filter Examples')
    lines += [f'- https://awesomereviewers.com/?repos={quote(r, safe="")}' for r in repos]
    lines += [f'- https://awesomereviewers.com/?categories={quote(c, safe="")}' for c in categories]
    lines += [f'- https://awesomereviewers.com/?languages={quote(l, safe="")}' for l in languages]
    with open('llms.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    reviewers, repos, categories, languages = collect_data()
    write_robots(reviewers, repos, categories, languages)
    write_llms(reviewers, repos, categories, languages)
