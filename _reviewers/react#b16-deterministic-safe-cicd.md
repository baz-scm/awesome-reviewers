---
title: Deterministic, Safe CI/CD
description: 'CI/CD workflows should be both safe to run and deterministic to execute:


  - Avoid risky defaults on release/publish actions (especially workflow_dispatch
  inputs that can change the release target). Require an explicit choice.'
repository: facebook/react#b16
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 251891
---

CI/CD workflows should be both safe to run and deterministic to execute:

- Avoid risky defaults on release/publish actions (especially workflow_dispatch inputs that can change the release target). Require an explicit choice.
- Don’t rely on GitHub-hosted base-image versions for external tools used by tests (e.g., Chrome/Chromium). Use the same browser binaries/version that Playwright uses (or an explicitly pinned version/artifact).

Example (workflow_dispatch without risky defaults):
```yml
on:
  workflow_dispatch:
    inputs:
      tag:
        description: npm dist-tag
        type: choice
        options: [latest, next]
        # no default to force explicit selection
      dry:
        description: Dry run
        type: boolean
        default: false
```

Example (don’t use base-image Chrome; use Playwright’s pinned browser):
```bash
# Instead of: /usr/bin/google-chrome --version
# Run version checks against the browser binaries Playwright installed/downloaded.
# (Exact command depends on your Playwright setup, but the key is: source from Playwright-managed binaries.)
```