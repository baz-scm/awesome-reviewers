---
title: Pin action commit hashes
description: Always pin third-party GitHub Actions to specific commit hashes rather
  than semantic version tags (like `@v1`). This prevents automatic execution of potentially
  malicious code if the maintainer updates the tag. Additionally, minimize permission
  scopes for any tokens used in workflows, and consider replacing third-party actions
  with direct implementations...
repository: expressjs/express
label: Security
language: Yaml
comments_count: 1
repository_stars: 67300
---

Always pin third-party GitHub Actions to specific commit hashes rather than semantic version tags (like `@v1`). This prevents automatic execution of potentially malicious code if the maintainer updates the tag. Additionally, minimize permission scopes for any tokens used in workflows, and consider replacing third-party actions with direct implementations when feasible.

Example - Instead of:
```yaml
- name: Repository Dispatch
  uses: peter-evans/repository-dispatch@v1
```

Use commit hash pinning:
```yaml
- name: Repository Dispatch
  uses: peter-evans/repository-dispatch@a328d6e8c37ac0b002f76abbdd3cfe2908502656
```

Even better, consider replacing with native functionality:
```yaml
- name: Repository Dispatch
  run: |
    curl -X POST \
      -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/owner/repo/dispatches \
      -d '{"event_type":"build_application"}'
```