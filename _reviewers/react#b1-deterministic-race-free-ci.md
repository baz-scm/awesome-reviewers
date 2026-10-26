---
title: Deterministic, Race-Free CI
description: 'CI workflows should be deterministic and race-free: pin external dependencies
  (especially browsers) to the exact versions your test stack expects, and use event
  triggers that match the specific PR state change you rely on.'
repository: facebook/react#b1
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251878
---

CI workflows should be deterministic and race-free: pin external dependencies (especially browsers) to the exact versions your test stack expects, and use event triggers that match the specific PR state change you rely on.

Apply this when adding/updating CI:
- Pin tool/runtime versions: if your tests run against Chrome/Chromium, don’t rely on the GitHub runner’s preinstalled “latest”. Prefer using the same browser version your Playwright version bundles (or otherwise lock Chrome to that known-good version).
- Make workflows trigger on the right event: if logic depends on a label/state being present, trigger on the corresponding GitHub event (e.g., label added), rather than running on PR opened and later hoping the label exists.

Example (race-free label-trigger pattern):
```yaml
name: Discord Notify

on:
  pull_request:
    types: [labeled]

jobs:
  notify:
    if: ${{ github.event.label.name == 'React Core Team' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Label added: ${{ github.event.label.name }}"
```

Example (pinned browser version principle):
- Don’t run tests using `/usr/bin/google-chrome` from the base image.
- Instead, use the Chrome/Chromium version aligned with Playwright (e.g., by extracting/using the Playwright-provided Chromium artifacts or locking Chrome to the same version).