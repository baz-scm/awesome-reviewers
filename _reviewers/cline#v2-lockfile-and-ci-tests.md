---
title: Lockfile and CI Tests
description: 'Ensure CI/CD is both reproducible and comprehensive.


  - **Reproducible dependency updates:** You may allow semver ranges (e.g., caret)
  in `package.json`, but CI builds must install from a **frozen/pinned lockfile**
  so the exact versions are deterministic. When you update dependency versions, update
  the lockfile **only to the versions you actually verified**...'
repository: cline/cline#v2
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70861
---

Ensure CI/CD is both reproducible and comprehensive.

- **Reproducible dependency updates:** You may allow semver ranges (e.g., caret) in `package.json`, but CI builds must install from a **frozen/pinned lockfile** so the exact versions are deterministic. When you update dependency versions, update the lockfile **only to the versions you actually verified** so PR scope stays tight.
- **Complete test wiring:** If you add or change a `test:*` script, verify CI runs it (don’t assume it executes). Also ensure any relevant cross-toolchain tests (e.g., `cargo test`) are included in the CI workflow when applicable.

Example (Node package):
```json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
Then enforce CI installs with a frozen lockfile (conceptually: “install from lockfile without allowing lockfile changes”), and ensure CI actually runs the corresponding test script(s), e.g. `pnpm/bun/yarn test:desktop-client`, plus any required `cargo test` step if the project includes Rust code.