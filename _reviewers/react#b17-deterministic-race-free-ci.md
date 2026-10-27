---
title: Deterministic, Race-Free CI
description: 'CI workflows should be deterministic and race-free: (1) pin runtime
  binaries/tooling to known versions from your test framework (or locked artifacts),
  and (2) trigger workflows on the exact GitHub event that represents the state change.'
repository: facebook/react#b17
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251891
---

CI workflows should be deterministic and race-free: (1) pin runtime binaries/tooling to known versions from your test framework (or locked artifacts), and (2) trigger workflows on the exact GitHub event that represents the state change.

**What to enforce**
- **Don’t rely on mutable runner images** for critical tools (e.g., Chrome/Chromium). Prefer the same version your test framework (e.g., Playwright) uses, to avoid random breaking changes.
- **Use precise workflow triggers** (e.g., `pull_request` with `types: [labeled]`) instead of triggering on `opened` and then conditionally checking label state—this avoids race conditions between label application and workflow execution.

**Example patterns**
- Pin Chrome/Chromium to Playwright’s version (conceptual):
```yaml
- name: Restore archived browser
  uses: actions/download-artifact@v4
  with:
    pattern: _playwright-browsers-*
    path: browsers

- name: Run tests
  run: |
    # Ensure Playwright/DevTools uses the pinned browser binaries
    yarn test:e2e
```
- Race-free label-triggered workflow:
```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  notify:
    if: ${{ github.event.label.name == 'React Core Team' }}
    runs-on: ubuntu-latest
```

Apply this as a standard when adding/updating CI workflows: verify tool versions come from stable sources, and verify the workflow fires based on the correct event type for the relevant state transition.