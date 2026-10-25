---
title: Ensure CI reproducibility
description: 'Keep CI pipelines deterministic and comprehensive:


  - Reproducible dependencies: allow `@ai-sdk/*` (or similar) dependencies to use
  caret ranges for normal maintenance, but ensure CI installs with a frozen lockfile
  so the build uses the exact pinned versions.'
repository: CLINE/cline
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70839
---

Keep CI pipelines deterministic and comprehensive:

- Reproducible dependencies: allow `@ai-sdk/*` (or similar) dependencies to use caret ranges for normal maintenance, but ensure CI installs with a frozen lockfile so the build uses the exact pinned versions.
- CI-wired tests: when you add a test script, also update the CI workflow to run it; don’t leave scripts unused. Verify all relevant ecosystems’ tests run (e.g., JS/TS tests via `vitest`, Rust via `cargo test`).

Example (package.json + CI wiring concept):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
In CI, make sure the step actually calls:
- `npm|bun|pnpm test:desktop-client` (or equivalent), and
- `cargo test` for Rust components.

Rule of thumb: PRs that change dependencies or tests must be accompanied by CI changes (or CI verification) so the pipeline runs with the intended versions and the intended test coverage.