---
title: Deterministic deps and CI tests
description: 'Ensure CI/CD is both deterministic and coverage-complete:


  1) Deterministic installs: If CI installs with a frozen lockfile, keep dependency
  updates aligned to what’s actually pinned in the lockfile. Use caret ranges as allowed,
  but don’t expand PR scope by unintentionally pulling newer transitive versions into
  the lock unless you intend to verify them.'
repository: cline/cline#v1
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70862
---

Ensure CI/CD is both deterministic and coverage-complete:

1) Deterministic installs: If CI installs with a frozen lockfile, keep dependency updates aligned to what’s actually pinned in the lockfile. Use caret ranges as allowed, but don’t expand PR scope by unintentionally pulling newer transitive versions into the lock unless you intend to verify them.

2) Coverage completeness: Any new or updated test scripts must be wired into the CI workflow so CI executes them. Adding `package.json` scripts without connecting them to CI leaves the change unverified.

Example (package scripts):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure your CI workflow runs `npm/bun/yarn run test:desktop-client` (or the repo’s equivalent test suite command). Also verify other relevant test runners (e.g., `cargo test` in Rust components) are invoked where applicable.

Apply this checklist before merging:
- Does CI install with a frozen lockfile, and does the lockfile reflect the intended dependency versions?
- Does CI call every newly added test script (and any other required test commands) so the PR is actually validated? 