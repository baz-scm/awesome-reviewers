---
title: Deterministic CI Workflow Rules
description: "All CI/CD workflows should be deterministic and correctness-safe:\n\n\
  - Standardize external runtime dependencies used by tests.\n  - Don’t rely on mutable\
  \ “runner” installed browser versions. Prefer the browser version shipped/managed\
  \ by your test toolchain (e.g., Playwright-managed Chromium) or explicitly pin the\
  \ version used in CI."
repository: facebook/react#b14
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 251893
---

All CI/CD workflows should be deterministic and correctness-safe:

- Standardize external runtime dependencies used by tests.
  - Don’t rely on mutable “runner” installed browser versions. Prefer the browser version shipped/managed by your test toolchain (e.g., Playwright-managed Chromium) or explicitly pin the version used in CI.
- Make workflow triggers and conditions precise.
  - Avoid brittle string parsing (e.g., `contains(..., '/land')`) when a command can appear in URLs or other text—use stricter patterns (e.g., anchored match / prefix match) to only react to the intended command.
- Avoid race conditions between workflows/events.
  - If behavior depends on a label, trigger on the labeled event rather than on PR-opened (or other earlier events) to ensure the label is present.
- Treat CI shell scripting as production code.
  - Escape shell-special characters in messages/log strings (e.g., backticks) so they don’t accidentally execute.
- Don’t add redundant checks.
  - If the invoked tool already enforces a constraint, prefer simpler logic unless you need a custom error message or additional policy.

Example (safe command check + escaped message):
```yaml
# Good: react only when the comment starts with the command
if: ${{ github.event.issue.pull_request && startsWith(github.event.comment.body, '/land') }}
```
```bash
# Good: escape backticks so they render instead of being executed
echo "Run \`yarn generate-inline-fizz-runtime\` and check in the result."
```