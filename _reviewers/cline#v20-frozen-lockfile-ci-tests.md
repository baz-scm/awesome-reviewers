---
title: Frozen lockfile CI tests
description: 'Ensure CI/CD runs deterministic builds and actually executes the test
  commands added for validation.


  Apply:

  1) Dependency determinism

  - If your build/CI uses a frozen lockfile, only bump dependency versions to what
  will be pinned by that lockfile.'
repository: cline/cline#v20
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70886
---

Ensure CI/CD runs deterministic builds and actually executes the test commands added for validation.

Apply:
1) Dependency determinism
- If your build/CI uses a frozen lockfile, only bump dependency versions to what will be pinned by that lockfile.
- Even if `package.json` uses caret ranges (e.g., `^5.x`), the CI-installed versions should come from the frozen lock (so the PR’s scope matches what CI verified).

2) Test execution in CI
- When you add a new `test:*` script (or a new test file), confirm the CI workflow calls it.
- If your repo has multiple ecosystems (e.g., Node + Rust), ensure CI runs tests for each (e.g., `cargo test` in addition to `vitest`).

Example (Node tests):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI workflow includes a step that runs `npm/yarn/bun run test:desktop-client` (or the equivalent command for your package manager).

Example (dependency bump alignment):
- Keep the `package.json` range broad if desired, but update the lockfile so CI’s frozen install pins the exact versions you intend to verify in that PR.