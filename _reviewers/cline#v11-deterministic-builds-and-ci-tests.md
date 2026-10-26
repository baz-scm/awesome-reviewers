---
title: Deterministic builds and CI tests
description: 'Ensure CI/CD changes are both deterministic and actually exercised:


  - Deterministic installs: Allow dependency version ranges (e.g., `^`) in package
  manifests, but make CI/builds install from a frozen lockfile so the CI result is
  reproducible (the lockfile, not the range, is what gets used).'
repository: cline/cline#v11
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70871
---

Ensure CI/CD changes are both deterministic and actually exercised:

- Deterministic installs: Allow dependency version ranges (e.g., `^`) in package manifests, but make CI/builds install from a frozen lockfile so the CI result is reproducible (the lockfile, not the range, is what gets used).
- Verified scope: When updating dependencies, only advance what’s been verified in CI/live builds; don’t broaden the lockfile range without intent.
- CI test coverage: If you add or modify a test script, wire it into the CI workflow so it runs automatically; avoid adding “orphan” scripts that never execute in CI.

Example (pattern for wiring a test script):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI pipeline calls `bun run test:desktop-client` (or the equivalent) as part of the test stage, and that install steps use a frozen lockfile (e.g., `--frozen-lockfile` where applicable).