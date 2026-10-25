---
title: Deterministic deps and tests
description: 'Ensure CI/CD runs with deterministic dependencies and executes all intended
  test suites.


  - Deterministic installs: keep dependency version intent in `package.json` (e.g.,
  caret ranges), but make CI (and release builds) install using the lockfile in frozen
  mode so results are reproducible.'
repository: CLINE/CLINE
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70837
---

Ensure CI/CD runs with deterministic dependencies and executes all intended test suites.

- Deterministic installs: keep dependency version intent in `package.json` (e.g., caret ranges), but make CI (and release builds) install using the lockfile in frozen mode so results are reproducible.
- Scope dependency updates: when you bump a dependency, update/commit the lockfile intentionally for the exact version validated by CI; avoid letting unrelated transitive changes silently expand PR scope.
- CI wiring for tests: any new or existing test script added to the project must be invoked by the CI workflow. Also verify non-JS test commands are covered when relevant (e.g., `cargo test` for Rust components).

Example patterns:
- Package manager install in CI should be “frozen lockfile” style (exact command depends on the tool):
  - `bun install --frozen-lockfile`
  - or `npm ci`
  - or `yarn install --frozen-lockfile`
- Add/enable CI steps to run test scripts explicitly (illustrative):
  - `bun run test:desktop-client`
  - `cargo test` (when the repository contains Rust code)