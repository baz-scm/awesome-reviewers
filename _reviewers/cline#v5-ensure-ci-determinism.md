---
title: Ensure CI determinism
description: 'CI should be the source of truth for what code and dependencies you
  actually test. To keep PR verification reliable and scoped:


  1) Pin what CI installs'
repository: cline/cline#v5
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70864
---

CI should be the source of truth for what code and dependencies you actually test. To keep PR verification reliable and scoped:

1) Pin what CI installs
- If your CI/build uses a frozen lockfile, ensure the lockfile contains only the intended dependency changes for the PR.
- When using caret ranges (e.g., `^5.0.98`), remember CI may install the locked version (e.g., `5.0.98`), so don’t rely on newer patch versions being exercised unless the lockfile is updated.

2) Wire tests into CI
- Any new test script added to `package.json` must be executed by the CI pipeline; otherwise it provides no protection.
- If the repo includes additional toolchains (e.g., Rust), ensure their test commands are also run in CI (e.g., `cargo test`).

Example (npm scripts + CI wiring intent)
```json
// package.json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure CI runs `pnpm/bun/npm run test:desktop-client` (and also runs other relevant suites like `cargo test` when applicable).