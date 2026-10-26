---
title: Deterministic CI Tests
description: 'Ensure CI verifies changes deterministically and completely:


  - **Deterministic dependencies:** You may use caret (`^`) ranges in `package.json`,
  but CI/install must use a **frozen lockfile** so resolved versions are reproducible.
  When updating dependencies, keep the **lockfile diff scoped to what you actually
  verified**.'
repository: cline/cline#v23
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70889
---

Ensure CI verifies changes deterministically and completely:

- **Deterministic dependencies:** You may use caret (`^`) ranges in `package.json`, but CI/install must use a **frozen lockfile** so resolved versions are reproducible. When updating dependencies, keep the **lockfile diff scoped to what you actually verified**.
- **Complete test execution:** Any newly added test scripts must be **wired into CI**. Also audit for missing language/tooling test runs (e.g., if the repo includes Rust, ensure `cargo test` is executed in CI).

Example (package-lock-scoped + CI-ready scripts):
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
In CI, ensure install is frozen (e.g., `--frozen-lockfile` / equivalent for your package manager) and that the relevant test commands (including `test:desktop-client` and, if applicable, `cargo test`) are invoked as steps.