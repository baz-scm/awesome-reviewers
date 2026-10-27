---
title: Pin tools and triggers
description: 'Apply this standard to CI/CD workflows to prevent flakiness and race
  conditions.


  1) Pin/derive external tool versions from the test framework

  - Avoid relying on the GitHub runner’s preinstalled versions (e.g., Chrome). Instead,
  use the exact browser version bundled/selected by Playwright.'
repository: facebook/react#b11
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 251894
---

Apply this standard to CI/CD workflows to prevent flakiness and race conditions.

1) Pin/derive external tool versions from the test framework
- Avoid relying on the GitHub runner’s preinstalled versions (e.g., Chrome). Instead, use the exact browser version bundled/selected by Playwright.

Example (instead of calling a random system Chrome):
```yaml
- name: Ensure browser version matches Playwright
  run: |
    # Use Playwright-managed Chromium for consistency
    npx playwright --version
    node -p "require('@playwright/test/package.json').version"
    # Your tests should launch via Playwright so the same browser is used.
```

2) Use the most reliable workflow event for state changes
- If behavior depends on a PR label (or any other state that another workflow changes), trigger directly on the corresponding event rather than on a less precise event that can race.

Example (label-driven notification):
```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  notify:
    if: ${{ github.event.label.name == 'React Core Team' }}
```

3) Make publish/release jobs safe and idempotent
- Guard against placeholder versions and avoid duplicate publishes (e.g., skip if the version already exists). Prefer only necessary checks; don’t duplicate what the publish command already guarantees.

General checklist
- No “system-installed” browser assumptions for browser-based tests.
- Workflow triggers map directly to the state change they depend on.
- Publish jobs refuse invalid versions and are safe to re-run.