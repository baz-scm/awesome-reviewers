---
title: Deterministic CI Tests
description: 'CI should be both deterministic and comprehensive: (1) lock down dependency
  resolution in CI, and (2) ensure all relevant tests are actually executed by the
  pipeline.'
repository: cline/cline#v16
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70882
---

CI should be both deterministic and comprehensive: (1) lock down dependency resolution in CI, and (2) ensure all relevant tests are actually executed by the pipeline.

**1) Deterministic builds**
- It’s acceptable to use caret ranges in `package.json`, as long as CI installs with a frozen lockfile so builds reproduce the same versions.
- When a PR updates dependencies, keep the lockfile scoped to the versions you’ve verified (avoid widening scope to unverified releases).

Example pattern:
```json
// package.json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
```sh
# CI install step (conceptually)
# e.g., npm ci / bun install --frozen-lockfile / yarn --frozen-lockfile
```

**2) Comprehensive test execution**
- Any new or existing test script that matters for correctness must be wired into CI.
- If you add scripts (e.g., `test:desktop-client`), ensure CI calls them.
- Also verify non-JS checks aren’t skipped accidentally (e.g., make sure `cargo test` runs when the repo contains Rust code).

Example wiring:
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure the CI job runs something equivalent to:
```sh
bun run test:desktop-client
cargo test
```

Adopt an explicit CI audit: every PR that changes dependencies or adds tests should confirm (via pipeline/job config) that the lockfile install is frozen and that the new/updated tests run in CI.