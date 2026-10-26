---
title: Untrusted Actions Checkout
description: 'Treat `pull_request_target` and `workflow_run` as *privileged* contexts:
  if you use them, you must assume any incoming PR code or artifacts are untrusted.'
repository: github/docs
label: Security
language: Markdown
comments_count: 6
repository_stars: 21111
---

Treat `pull_request_target` and `workflow_run` as *privileged* contexts: if you use them, you must assume any incoming PR code or artifacts are untrusted.

Coding standard:
- Prefer safer triggers (for example, `pull_request`) unless you truly need privileged access.
- If you use `pull_request_target` or `workflow_run`, **do not check out, build, or run untrusted code** (including PR forks or repositories you don’t control).
- For `workflow_run`, treat artifacts uploaded by other workflows as untrusted.
- Ensure steps that would use untrusted content are gated/removed entirely in these workflows.

Example (safe pattern: no PR checkout; only operate on trusted base code):
```yaml
on:
  pull_request_target:

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      # Do NOT checkout the PR’s head/contents here.
      # Use the checked-out base repo (default) or avoid checkout entirely.
      - name: Run security checks on trusted base
        run: |
          echo "Do work without executing PR-provided code"
```

If your workflow truly needs to run code from the PR, use `pull_request` (or a separate, non-privileged workflow) for that execution path and keep the privileged workflow restricted to non-executable, trusted operations.