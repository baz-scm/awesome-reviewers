---
title: Deterministic CI Testing
description: 'Ensure CI is both reproducible and actually executes the tests you add.


  - Dependency determinism: If you use semver ranges (e.g., `^5.0.98`) in `package.json`,
  make CI/builds install with a *frozen lockfile* so the resolved versions are consistent.
  When updating dependencies, only advance the lockfile to versions you have verified;
  avoid widening the lock...'
repository: cline/cline#v12
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70872
---

Ensure CI is both reproducible and actually executes the tests you add.

- Dependency determinism: If you use semver ranges (e.g., `^5.0.98`) in `package.json`, make CI/builds install with a *frozen lockfile* so the resolved versions are consistent. When updating dependencies, only advance the lockfile to versions you have verified; avoid widening the lock to nearby patch/minor versions “just because” they satisfy the range.

- CI coverage: Any new or modified test script should be wired into the CI workflow the same PR, and pipeline checks should confirm all intended suites run (including non-JS tooling like `cargo test`).

Example (wiring a new test into CI):
```json
// apps/examples/desktop-app/package.json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then, ensure your CI command list includes it (and also runs `cargo test` if the repo has Rust components).

Checklist:
1) CI installs with frozen lockfile (no unexpected dependency drift).
2) PR dependency updates include deliberate lockfile changes only for validated versions.
3) CI runs all relevant test commands, including any newly added `test:*` scripts and `cargo test` where applicable.