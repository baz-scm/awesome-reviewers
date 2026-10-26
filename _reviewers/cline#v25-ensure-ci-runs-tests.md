---
title: Ensure CI runs tests
description: 'Add (and verify) any new or meaningful test commands to your CI pipeline;
  updating `package.json` scripts alone isn’t enough.


  Practical application:

  - When you add a script like `test:desktop-client`, also update the CI workflow
  to run it (and fail the build on test failures).'
repository: cline/cline#v25
label: CI/CD
language: Json
comments_count: 2
repository_stars: 70891
---

Add (and verify) any new or meaningful test commands to your CI pipeline; updating `package.json` scripts alone isn’t enough.

Practical application:
- When you add a script like `test:desktop-client`, also update the CI workflow to run it (and fail the build on test failures).
- If your CI uses a frozen lockfile, keep dependency updates consistent with the locked versions used by CI to preserve reproducibility.

Example (typical CI wiring for the new Vitest script):
```yaml
# .github/workflows/ci.yml (example)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run test:desktop-client
      - run: bun run test:settings-ui
      - run: bun run test:sidecar
```
This ensures CI coverage matches what developers and reviewers intend, and builds remain deterministic via the lockfile.