---
title: Deterministic CI/CD Automation
description: 'When changing CI/CD workflows (build, test, publish), ensure automation
  is deterministic and robust:


  - **Pin tool-dependent runtime versions**: For browser/E2E tests, don’t rely on
  runner-provided Chrome versions. Use the exact Chrome/Chromium version that matches
  your Playwright toolchain (or reuse Playwright’s archived Chromium). If you can’t
  reuse...'
repository: facebook/react#b4
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 251885
---

When changing CI/CD workflows (build, test, publish), ensure automation is deterministic and robust:

- **Pin tool-dependent runtime versions**: For browser/E2E tests, don’t rely on runner-provided Chrome versions. Use the exact Chrome/Chromium version that matches your Playwright toolchain (or reuse Playwright’s archived Chromium). If you can’t reuse binaries, explicitly install/pin the same Chrome version Playwright expects.

- **Use precise trigger/command matching**: Don’t rely on broad substring checks for workflow triggers (e.g., checking whether text *contains* `/land`). Prefer strict matching (e.g., `startsWith`, regex with word boundaries) so URLs or unrelated text don’t accidentally trigger deployments/land operations.

- **Avoid redundant prechecks**: If the underlying tool already enforces the constraint (e.g., `npm publish` validates publishability), don’t duplicate those checks in the workflow—focus workflow logic on protections/guardrails that the tool doesn’t cover (e.g., refusing placeholder versions, protected environments, skipping already-published versions).

Example patterns:

```yaml
# Strict command matching (avoid accidental /land in URLs)
# Good: start-of-line or whole-command match
if: ${{ github.event.issue.pull_request && startsWith(github.event.comment.body, '/land') }}

# E2E: pin Chrome to the Playwright-matched version (conceptual)
# Install the same browser version used by your Playwright setup, rather than
# whatever the base image provides.
# (Implementation varies by repo; the key is version parity with Playwright.)
```

Apply this standard to keep CI/CD reliable (fewer flaky E2E failures), safer (fewer accidental triggers), and simpler (less redundant workflow logic).