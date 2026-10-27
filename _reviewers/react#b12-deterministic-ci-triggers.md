---
title: Deterministic CI Triggers
description: 'CI pipelines should be deterministic and race-free to avoid flaky test
  behavior and “surprise” environment changes.


  **1) Pin external runtimes/tools**'
repository: facebook/react#b12
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251896
---

CI pipelines should be deterministic and race-free to avoid flaky test behavior and “surprise” environment changes.

**1) Pin external runtimes/tools**
- Don’t rely on versions from GitHub’s base images (e.g., `ubuntu-latest` Chrome can change).
- Use the same browser version your Playwright setup uses (or the exact Chromium binaries produced by your Playwright install), so E2E tests run against a consistent target across all jobs.

Example (pattern):
```yaml
- name: Check Chrome version
  run: |
    # Prefer the version shipped/used by Playwright, not the OS image
    npx playwright --version
    # or point to the Playwright-managed Chromium/Chrome binary version
```

**2) Use race-free workflow triggers**
- For label-driven automation, trigger on the label event (e.g., PR labeled) rather than checking label state during `pull_request` opened.
- This prevents timing races between workflows that add labels and workflows that react to them.

Example (pattern):
```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  notify:
    if: ${{ github.event.label.name == 'React Core Team' }}
```

Apply this checklist whenever you add/modify CI: (a) verify that all external dependencies are pinned/consistent, and (b) ensure the workflow trigger is event-accurate and not dependent on state updates arriving in time.