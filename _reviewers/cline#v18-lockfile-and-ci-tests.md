---
title: Lockfile and CI tests
description: 'Ensure CI/CD is both deterministic and comprehensive:


  1) Deterministic installs

  - Keep desired version flexibility in `package.json` (e.g., caret ranges), but make
  CI install from a frozen lockfile so the exact versions used are pinned.'
repository: cline/cline#v18
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70884
---

Ensure CI/CD is both deterministic and comprehensive:

1) Deterministic installs
- Keep desired version flexibility in `package.json` (e.g., caret ranges), but make CI install from a frozen lockfile so the exact versions used are pinned.
- Update the lockfile intentionally when you change dependency versions, and avoid expanding scope by pulling in additional lock updates.

Example:
```json
// package.json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
And ensure CI uses a frozen/locked install (conceptually: `npm ci` / `bun install --frozen-lockfile` / `pnpm install --frozen-lockfile`).

2) Test commands must run in CI
- If a new test script is added (e.g., `vitest run ...`), wire it into the CI workflow so it actually executes.
- If the repo includes other ecosystems, ensure their tests also run (e.g., don’t forget `cargo test` when Rust code exists).

Example (package.json scripts):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then make sure your CI pipeline calls `npm run test:desktop-client` (or the equivalent for your package manager), and add `cargo test` steps where applicable.