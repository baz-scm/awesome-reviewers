---
title: Deterministic CI Verification
description: 'Ensure CI uses deterministic inputs and runs the full set of intended
  verification.


  - Dependency determinism: it’s acceptable to keep semver ranges (e.g., `^`) in `package.json`
  as long as CI/builds install using a frozen lockfile, so the versions actually tested
  are locked and reproducible. When bumping a dependency, keep the lockfile changes
  scoped to...'
repository: cline/cline#v3
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70863
---

Ensure CI uses deterministic inputs and runs the full set of intended verification.

- Dependency determinism: it’s acceptable to keep semver ranges (e.g., `^`) in `package.json` as long as CI/builds install using a frozen lockfile, so the versions actually tested are locked and reproducible. When bumping a dependency, keep the lockfile changes scoped to what you’ve verified; avoid broad lock updates you haven’t tested.

- Test coverage: if a test script exists (or is added), make sure it is invoked by CI. Don’t leave important tests “orphaned” behind local scripts. Also ensure other language toolchains in the repo (e.g., Rust) are covered (e.g., run `cargo test` if applicable).

Example (JS/TS):
```json
// package.json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  },
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
In CI, ensure installs are locked (frozen) and that `test:desktop-client` is included in the CI test command(s).

Example (Rust):
```bash
# CI step (only if the repo includes Rust)
cargo test
```