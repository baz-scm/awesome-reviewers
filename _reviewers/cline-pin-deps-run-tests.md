---
title: Pin deps, run tests
description: 'For CI/CD, make builds deterministic and ensure verification steps actually
  run.


  - Dependency determinism: allow semver ranges in `package.json` (e.g., caret), but
  require CI to install using a frozen/pinned lockfile so the resolved versions are
  consistent across runs.'
repository: Cline/Cline
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70840
---

For CI/CD, make builds deterministic and ensure verification steps actually run.

- Dependency determinism: allow semver ranges in `package.json` (e.g., caret), but require CI to install using a frozen/pinned lockfile so the resolved versions are consistent across runs.
  - Example: keep `"@ai-sdk/amazon-bedrock": "^5.x"` in `package.json`, but configure CI to install with a frozen lockfile (so CI uses exactly what’s in `lockfile` for that PR).

- CI test wiring: if you add or rename a `package.json` test script, update the CI workflow so it executes.
  - Example `package.json`:
    ```json
    {
      "scripts": {
        "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
      }
    }
    ```
  - Then in CI, add a step that runs `bun run test:desktop-client` (or the equivalent for your runner).

- Coverage checks: explicitly include all relevant test suites (e.g., JS/TS tests and Rust `cargo test`)—don’t assume they run automatically.

This prevents “it passed locally” issues from both nondeterministic dependency resolution and missing CI verification steps.