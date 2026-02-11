---
title: limit CI tokens
description: Always prefer the built-in GITHUB_TOKEN, explicitly document why it’s
  needed, and grant it only the minimum permissions required. For third‑party actions
  that call the GitHub API, pin them and justify token usage in the workflow so reviewers
  can verify scope and intent.
repository: p-e-w/heretic
label: Security
language: Yaml
comments_count: 1
repository_stars: 5002
---

Always prefer the built-in GITHUB_TOKEN, explicitly document why it’s needed, and grant it only the minimum permissions required. For third‑party actions that call the GitHub API, pin them and justify token usage in the workflow so reviewers can verify scope and intent.

Why: automatic tokens are safer than adding shared secrets; minimizing permissions reduces blast radius if an action is compromised; pinning and documenting lets reviewers assess supply‑chain risk.

How to apply:
- Use GITHUB_TOKEN instead of custom secrets when possible.
- Explicitly set repository permissions to the least privilege needed (example below sets read-only access to pull requests).
- Pin actions to a specific version/release and include a short comment explaining why the token is required.
- Prefer pull_request over pull_request_target unless you explicitly need base-repo context; if using pull_request_target, be extra cautious because it runs in the base repo context.

Example (from discussion):
name: Lint PR

on:
  pull_request_target:
    types: [opened, reopened, edited]

jobs:
  main:
    name: Validate PR title
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read    # minimal permission needed to read PR metadata
    steps:
      - uses: amannn/action-semantic-pull-request@v6  # pin action
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # builtin token; documented above

Checklist for reviewers:
- Is GITHUB_TOKEN required? Is the reason documented?
- Are permissions scoped to the minimum (read vs write)?
- Is the action pinned and from a trusted source?
- Could pull_request be used instead of pull_request_target to reduce risk?

References: [0]