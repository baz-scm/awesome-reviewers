---
title: Enforce CI Reproducibility
description: 'In CI/CD, guarantee reproducible builds and actionable test coverage:


  1) Dependency bumps must be reproducible and scope-controlled

  - Keep semver ranges (e.g., ^x.y.z) in package.json, but ensure CI installs from
  the lockfile using a frozen/CI-safe mode (e.g., “frozen lockfile”) so the exact
  versions used are pinned and consistent.'
repository: cline/cline#v15
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70877
---

In CI/CD, guarantee reproducible builds and actionable test coverage:

1) Dependency bumps must be reproducible and scope-controlled
- Keep semver ranges (e.g., ^x.y.z) in package.json, but ensure CI installs from the lockfile using a frozen/CI-safe mode (e.g., “frozen lockfile”) so the exact versions used are pinned and consistent.
- When bumping lock-resolved versions, only include versions that were verified for that PR; avoid widening the range beyond what you’ve validated.

2) Every meaningful test script must run in CI
- If you add a test script (or a new test file), update the CI workflow so CI actually executes it—local script availability is not enough.

Example (package.json script + intended CI wiring):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI job calls something like `bun test:desktop-client` / `npm run test:desktop-client` (alongside the existing test scripts), and that dependency installation uses a frozen lockfile mode.

Apply this standard to prevent “works on CI” mismatches caused by lock/version drift and to prevent regressions from landing because new tests weren’t executed by CI.