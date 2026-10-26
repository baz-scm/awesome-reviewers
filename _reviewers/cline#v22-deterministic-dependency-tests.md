---
title: Deterministic Dependency + Tests
description: 'Ensure CI pipelines use deterministic inputs and run the tests you add.


  1) Deterministic dependency updates (lockfile-first)

  - Allow semver ranges in manifests, but CI/builds must install from the lockfile
  with a frozen policy.'
repository: cline/cline#v22
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70886
---

Ensure CI pipelines use deterministic inputs and run the tests you add.

1) Deterministic dependency updates (lockfile-first)
- Allow semver ranges in manifests, but CI/builds must install from the lockfile with a frozen policy.
- When updating dependencies, keep the lockfile changes scoped to what you actually verified (avoid accidentally pulling newer transitive versions in CI).

Example (package.json dependency range + frozen-lockfile install in CI):
```json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
In CI, install with a frozen lockfile (exact command depends on your tooling, but the requirement is “frozen lockfile” so the resolved version matches the committed lockfile).

2) CI wiring for tests (no “local-only” scripts)
- Any new test script you add should be executed in CI (JS/Vitest, Rust/cargo test, etc.).
- Add/confirm CI steps that call those scripts so missing coverage is caught before merge.

Example (adding a test script, then ensure CI runs it):
```json
{
  "scripts": {
    "test:desktop-client": "vitest run webview/lib/desktop-client.test.ts --config vitest.config.ts"
  }
}
```
Then include a CI step that runs the script (and ensure other stacks like Rust run `cargo test` if applicable).