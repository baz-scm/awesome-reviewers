---
title: Ensure CI determinism
description: 'CI/CD should be both deterministic and complete: lock dependencies predictably
  and ensure every relevant test script actually runs in the pipeline.


  - Dependency determinism: it’s acceptable to use caret ranges for @ai-sdk/* (or
  similar) if CI/install uses a frozen lockfile, so the build always resolves to the
  lockfile-pinned versions.'
repository: cline/cline#v27
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70892
---

CI/CD should be both deterministic and complete: lock dependencies predictably and ensure every relevant test script actually runs in the pipeline.

- Dependency determinism: it’s acceptable to use caret ranges for @ai-sdk/* (or similar) if CI/install uses a frozen lockfile, so the build always resolves to the lockfile-pinned versions.
- Test completeness: when you add a new test script, update the CI workflow (or the command list it uses) to run it; don’t rely on developers running it locally.
- Coverage sanity checks: verify all relevant test suites are represented (e.g., JS/TS tests and `cargo test` if you have Rust code); missing commands should be treated as CI bugs.

Example (package.json + CI wiring sketch):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then ensure the CI workflow includes a step that runs `bun run test:desktop-client` (and other relevant test scripts), and that your dependency installation uses a frozen lockfile (e.g., `bun install --frozen-lockfile` or the equivalent for your tooling).