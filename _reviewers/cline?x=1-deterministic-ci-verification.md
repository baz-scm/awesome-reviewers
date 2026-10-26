---
title: Deterministic CI Verification
description: 'Ensure CI validates exactly what you intend to ship by combining deterministic
  dependency installation with explicit test execution.


  - Dependency changes: Prefer keeping semver ranges in package.json (e.g., `^x.y.z`),
  but make CI/builds install using a frozen lockfile so the resolved versions are
  deterministic. If you intentionally exclude newer...'
repository: cline/cline?x=1
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70861
---

Ensure CI validates exactly what you intend to ship by combining deterministic dependency installation with explicit test execution.

- Dependency changes: Prefer keeping semver ranges in package.json (e.g., `^x.y.z`), but make CI/builds install using a frozen lockfile so the resolved versions are deterministic. If you intentionally exclude newer patch/minor versions to keep PR scope small, do it by controlling what’s committed in the lockfile.
- Test changes: Don’t add/modify test scripts unless CI actually runs them. Update the CI workflow (or test runner configuration) to invoke the new/changed test commands, and confirm all relevant suites run (including non-default ecosystems if present).

Example (package.json + frozen lockfile expectation):
```json
{
  "dependencies": {
    "@ai-sdk/amazon-bedrock": "^5.0.98"
  }
}
```
CI/build should then run installs with a frozen lockfile so the build uses the locked `5.0.98` resolution rather than whatever the caret might allow.

Example (CI wiring idea):
- If you add `test:desktop-client`, ensure CI’s test step runs it (or calls a script that includes it), instead of only running a subset of `vitest` commands.