---
title: Reproducible CI and Tests
description: 'Ensure CI/CD is both reproducible and actually validates what you change.


  - Reproducible dependencies: Run CI installs with a frozen lockfile so resolved
  versions are pinned. If you update a dependency range, make sure the lockfile resolves
  to the specific version you’ve verified; avoid expanding the lock to unverified
  patch versions just to satisfy semver...'
repository: cline/cline#v19
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70885
---

Ensure CI/CD is both reproducible and actually validates what you change.

- Reproducible dependencies: Run CI installs with a frozen lockfile so resolved versions are pinned. If you update a dependency range, make sure the lockfile resolves to the specific version you’ve verified; avoid expanding the lock to unverified patch versions just to satisfy semver ranges.
- Complete test coverage: Any new test script you add should be wired into CI so it runs automatically. Also confirm CI runs all relevant test commands (including any non-JS suites used by the repo).

Example (workflow-level intent):
- Install with frozen lockfile (conceptually):
  - `install --frozen-lockfile`
- Add the new test script to CI:
  - `vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts`