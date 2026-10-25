---
title: Deterministic Builds, Verified Tests
description: 'In CI/CD, keep builds reproducible and ensure newly added verification
  steps actually run.


  1) Dependency determinism via frozen lockfiles

  - It’s OK to use caret ranges in `package.json` (e.g., `@ai-sdk/*`), but CI/builds
  must install with a frozen lockfile so the resolved versions are pinned and PR scope
  stays predictable.'
repository: ClInE/cLiNe
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70838
---

In CI/CD, keep builds reproducible and ensure newly added verification steps actually run.

1) Dependency determinism via frozen lockfiles
- It’s OK to use caret ranges in `package.json` (e.g., `@ai-sdk/*`), but CI/builds must install with a frozen lockfile so the resolved versions are pinned and PR scope stays predictable.
- If you intentionally exclude newer versions from the lockfile to match what you tested, do so explicitly and keep the change set limited.

2) CI must execute relevant tests
- Adding a script (e.g., `test:desktop-client`) is not sufficient—update the CI workflow so CI calls it.
- Periodically audit CI to confirm all expected suites run (including non-JS suites like `cargo test`).

Example (wiring a test script into CI)
```json
// package.json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI job includes a step like:
```sh
bun run test:desktop-client
```

Example (frozen lockfile install)
```sh
bun install --frozen-lockfile
# or npm ci / yarn --frozen-lockfile, depending on your toolchain
```

Apply this rule to every CI/CD PR: (a) resolve dependency changes deterministically, and (b) wire verification scripts so CI provides real coverage.