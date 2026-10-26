---
title: Deterministic dependencies and CI tests
description: 'Ensure CI/CD runs are reproducible and that test changes actually execute
  in CI.


  - Use a frozen lockfile in CI (e.g., npm/yarn/pnpm “frozen-lockfile” / Bun equivalent)
  so semver caret ranges in package.json resolve to the exact versions pinned by the
  lockfile.'
repository: cline/cline#v26
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70893
---

Ensure CI/CD runs are reproducible and that test changes actually execute in CI.

- Use a frozen lockfile in CI (e.g., npm/yarn/pnpm “frozen-lockfile” / Bun equivalent) so semver caret ranges in package.json resolve to the exact versions pinned by the lockfile.
- When updating dependencies, keep PR scope aligned with what was verified: pin only the locked version(s) you intend to validate.
- When adding a new test script (or modifying existing ones), wire it into the CI workflow in the same PR so it runs automatically.

Example (package.json):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```

Example (CI job step conceptually):
```sh
# Install deterministically
bun install --frozen-lockfile

# Run all intended tests, including new ones
bun run test:desktop-client
```