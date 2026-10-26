---
title: Pin CI Actions By SHA
description: 'When writing CI/CD workflows (and the documentation snippets that users
  copy/paste), always:


  - **Pin every third-party GitHub Action to an immutable commit SHA** (optionally
  with a comment showing the intended version), instead of using only tags like `@v4`.'
repository: github/docs
label: CI/CD
language: Markdown
comments_count: 8
repository_stars: 21111
---

When writing CI/CD workflows (and the documentation snippets that users copy/paste), always:

- **Pin every third-party GitHub Action to an immutable commit SHA** (optionally with a comment showing the intended version), instead of using only tags like `@v4`.
- **Use secure authentication patterns** (for example, OIDC) and avoid long-lived credentials when supported.
- **Ensure examples are paste-ready by correctly escaping**:
  - Expression interpolation in docs build systems/secrets (wrap with the required raw markers/escaping so `${{ ... }}` is rendered correctly for the final YAML).
  - Glob/metacharacters in event filters like `workflow_run.workflows` (escape special characters such as `+` with `\+`).

Example (pinned actions + OIDC output usage):
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Get Docker OIDC token
    uses: docker/oidc-action@3f002d200df5620744c973221788e401898c6f86 # v1
    with:
      connection_id: YOUR_CONNECTION_ID

  - name: Sign in to Docker Hub
    uses: docker/login-action@af1e73f918a031802d376d3c8bbc3fe56130a9b0 # v4.4.0
    with:
      username: YOUR_DOCKER_ORG
      password: ${{ steps.docker-oidc.outputs.token }}
```

Example (escaping glob characters for `workflow_run`):
```yaml
on:
  workflow_run:
    workflows: ["Build C\+\+"]
    types: [completed]
```