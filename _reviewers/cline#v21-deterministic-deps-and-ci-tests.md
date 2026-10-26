---
title: Deterministic deps and CI tests
description: 'Ensure CI/CD is both reproducible and comprehensive:


  - **Deterministic installs:** It’s OK to use caret (`^`) ranges in `package.json`,
  but CI builds must install from a **frozen/pinned lockfile** so the actual dependency
  graph is reproducible.'
repository: cline/cline#v21
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70886
---

Ensure CI/CD is both reproducible and comprehensive:

- **Deterministic installs:** It’s OK to use caret (`^`) ranges in `package.json`, but CI builds must install from a **frozen/pinned lockfile** so the actual dependency graph is reproducible.
- **Scoped dependency PRs:** When you update dependency versions, keep the PR scope aligned with what CI/live verification will actually test via the lockfile (don’t “pre-advance” versions that aren’t represented in the locked build).
- **Test wiring:** Any new test script you add (e.g., `test:desktop-client`) must be **called by CI**. If CI doesn’t run it, the script is effectively dead—update the pipeline. Also audit for missing language/tooling test steps (e.g., `cargo test`).

Example pattern:

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

```sh
# CI install (must be frozen/pinned)
# (Exact command depends on your package manager)
# e.g., npm ci / bun install --frozen-lockfile / pnpm i --frozen-lockfile

# CI test invocation (must include newly added scripts)
# e.g., bun run test:desktop-client
# and ensure other test runners are covered (e.g., cargo test) where applicable
```