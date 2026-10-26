---
title: CI determinism and tests
description: 'All CI pipelines must be reproducible and must actually run the project’s
  relevant tests.


  - Reproducible installs: Allow permissive version ranges in manifest files, but
  ensure CI installs with a frozen lockfile so the exact dependency versions used
  in CI are pinned. Update the lockfile only when the PR’s scope includes dependency
  changes.'
repository: cline/cline#v17
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70883
---

All CI pipelines must be reproducible and must actually run the project’s relevant tests.

- Reproducible installs: Allow permissive version ranges in manifest files, but ensure CI installs with a frozen lockfile so the exact dependency versions used in CI are pinned. Update the lockfile only when the PR’s scope includes dependency changes.
  - Example (manifest uses a caret range, lockfile pins exact versions via frozen installs):
    ```json
    {
      "dependencies": {
        "@ai-sdk/amazon-bedrock": "^5.0.98"
      }
    }
    ```
    Ensure CI uses a frozen lockfile (e.g., `bun install --frozen-lockfile`, `npm ci`, etc.).

- Verified test coverage: Any new/important test script (e.g., `test:desktop-client`) must be wired into CI, and CI configuration must not silently omit other ecosystems’ suites (e.g., avoid situations where `cargo test` is never run).
  - Action: when adding a test script in `package.json`, also update the CI workflow to execute it (and confirm no separate test runner is neglected).