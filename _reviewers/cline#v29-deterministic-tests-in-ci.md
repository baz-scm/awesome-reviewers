---
title: Deterministic Tests in CI
description: "Ensure CI/CD runs deterministic builds and covers the tests you add.\n\
  \n- Deterministic dependency installs:\n  - Use frozen lockfile installs in CI so\
  \ semver ranges in package.json don’t introduce variability at build time."
repository: cline/cline#v29
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70893
---

Ensure CI/CD runs deterministic builds and covers the tests you add.

- Deterministic dependency installs:
  - Use frozen lockfile installs in CI so semver ranges in package.json don’t introduce variability at build time.
  - When bumping `@ai-sdk/*` (or similar) dependencies, keep the PR scoped to versions actually present in the lockfile you verified.

- No orphaned test scripts:
  - After adding a new test command in `package.json`, wire it into your CI workflow so it actually runs.
  - If your repo includes other ecosystems (e.g., Rust), confirm their test commands are also executed (e.g., `cargo test`) as part of CI.

Example (package.json + CI wiring concept):
```json
// package.json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI pipeline invokes that script (and any other relevant ones), while dependency installation uses a frozen lockfile (e.g., `npm ci` / `bun install --frozen-lockfile` / `yarn install --frozen-lockfile`, depending on your tooling).