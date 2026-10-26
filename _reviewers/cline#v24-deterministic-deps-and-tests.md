---
title: Deterministic deps and tests
description: 'CI should be both reproducible and comprehensive.


  1) Make dependency installs deterministic in CI

  - Allow caret ranges in `package.json`, but ensure CI/builds install using a frozen
  lockfile so the actual resolved versions are fixed.'
repository: cline/cline#v24
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70891
---

CI should be both reproducible and comprehensive.

1) Make dependency installs deterministic in CI
- Allow caret ranges in `package.json`, but ensure CI/builds install using a frozen lockfile so the actual resolved versions are fixed.

Example (typical Node/Bun/lockfile approach):
```sh
# Ensure CI does not update the lockfile and stays pinned to it
# (use the equivalent frozen/ci mode for your package manager)
package-manager install --frozen-lockfile
```

2) Wire new/important tests into CI
- If a test script is added (e.g., a new `vitest` command), update the CI workflow so it runs automatically; don’t rely on ad-hoc local execution.
- Also verify cross-language suites are covered where applicable (e.g., if the repo includes Rust, ensure `cargo test` is invoked in CI).

3) Checklist for PRs
- Dependencies: Are CI install steps using frozen lockfiles?
- Tests: Are all newly added/modified test scripts executed in CI workflows?
- Coverage: Any existing expected suite missing from CI (e.g., `cargo test`)?
