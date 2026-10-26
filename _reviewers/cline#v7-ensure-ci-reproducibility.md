---
title: Ensure CI Reproducibility
description: 'CI/CD should run the exact dependency set and test commands that the
  PR claims to validate.


  Apply these rules:

  1) Reproducible dependencies: If you allow version ranges (e.g., caret `^`) in `package.json`,
  CI builds must install from a frozen lockfile so the resolved versions are deterministic.'
repository: cline/cline#v7
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70865
---

CI/CD should run the exact dependency set and test commands that the PR claims to validate.

Apply these rules:
1) Reproducible dependencies: If you allow version ranges (e.g., caret `^`) in `package.json`, CI builds must install from a frozen lockfile so the resolved versions are deterministic.
2) Scope control: When bumping dependencies, ensure the PR changes only what CI is actually exercising (avoid widening the verified surface unintentionally).
3) Tests must run in CI: Any new `npm`/`bun`/`vitest` (or equivalent) test script should be wired into CI; don’t add scripts that only work locally.
4) Multi-language test audit: If the repo includes other ecosystems (e.g., Rust), ensure CI runs their test commands too.

Example (Node):
- Keep caret ranges in `package.json`, but guarantee CI uses a frozen lockfile:

```json
// package.json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```

- In CI, use frozen lockfile installs (conceptually):
  - `bun install --frozen-lockfile`
  - or `npm ci`

Example (tests):
- If you add `test:desktop-client`, ensure the CI job runs it (e.g., `bun run test:desktop-client`) instead of leaving it unused outside local runs.