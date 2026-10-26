---
title: Deterministic Dependencies and Tests
description: 'CI/CD should both (1) be deterministic about what code and dependencies
  run, and (2) reliably execute the tests developers add.


  Apply these rules:

  - Deterministic installs: If package.json uses caret ranges, CI/builds must install
  using a frozen lockfile so the effective dependency versions come from the lockfile
  (not from semver drift).'
repository: cline/cline#v30
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70894
---

CI/CD should both (1) be deterministic about what code and dependencies run, and (2) reliably execute the tests developers add.

Apply these rules:
- Deterministic installs: If package.json uses caret ranges, CI/builds must install using a frozen lockfile so the effective dependency versions come from the lockfile (not from semver drift).
- Test coverage wiring: Any new `package.json` test script must be executed by CI. Also ensure non-JS test suites (e.g., Rust) are included (e.g., `cargo test`), so adding code doesn’t leave it untested.

Example CI checks (conceptual):
```bash
# Deterministic dependency installation
# (choose your package manager equivalents)
lockfile-install --frozen-lockfile

# Ensure all relevant tests run in CI
npm run test:desktop-client
npm run test:settings-ui
cargo test
```