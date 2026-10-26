---
title: Deterministic deps and tests
description: 'Ensure CI/CD is both reproducible and comprehensive:


  1) Deterministic dependency installs

  - It’s acceptable to use caret ranges in `package.json`, but CI must install from
  a frozen/pinned lockfile so builds are repeatable.'
repository: cline/cline#x
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70861
---

Ensure CI/CD is both reproducible and comprehensive:

1) Deterministic dependency installs
- It’s acceptable to use caret ranges in `package.json`, but CI must install from a frozen/pinned lockfile so builds are repeatable.
- When bumping `@.../sdk`-style dependencies, update only to the versions you’ve verified in the lockfile; avoid widening scope by pulling additional unverified versions.

2) CI must run the tests you add
- If you add a test script/command, confirm the CI workflow calls it. Don’t leave “dead” scripts unexecuted.
- Ensure all relevant ecosystems’ tests are covered (e.g., if there’s Rust code, CI should run `cargo test`, not just JS/TS tests).

Example (package + CI wiring intent)
- `package.json` may use caret:
```json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
- CI should install with a frozen lockfile (conceptually):
```sh
# CI
# install using the pinned lockfile so caret ranges don’t change what actually builds
install --frozen-lockfile
```
- Any added test script must be referenced by CI; otherwise either wire it into the workflow or omit it from the PR.