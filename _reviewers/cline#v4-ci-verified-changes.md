---
title: CI-verified changes
description: 'When making PRs that affect builds or behavior, ensure the CI pipeline
  actually validates the same inputs you’re changing.


  1) Dependency bumps: verify against the pinned lockfile'
repository: cline/cline#v4
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70864
---

When making PRs that affect builds or behavior, ensure the CI pipeline actually validates the same inputs you’re changing.

1) Dependency bumps: verify against the pinned lockfile
- If your build uses a frozen lockfile, then the effective dependency versions are the lockfile-pinned ones (even if package.json uses caret ranges).
- Keep PR scope aligned with what the frozen-lockfile build will install, and avoid claiming validation for versions that aren’t in the lock.

2) Test scripts: wire new tests into CI
- Adding a test script is not enough—ensure CI calls it.
- If a test suite (including non-JS like cargo test) isn’t running in CI, either enable it or explicitly document why.

Example (wiring a new test into CI):
- package.json:
  {
    "scripts": {
      "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
    }
  }
- CI workflow (conceptually): run `bun test:desktop-client` (or the repo’s standard test command) in the test job so the new coverage executes on every PR.