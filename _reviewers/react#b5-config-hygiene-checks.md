---
title: Config hygiene checks
description: 'Keep configuration artifacts (ignore rules, dependency wiring, lockfiles)
  consistent with the real paths/sources used in builds.


  Apply:

  - **Validate path coverage for globs/ignore rules**: ensure patterns match the actual
  directory depth.'
repository: facebook/react#b5
label: Configurations
language: Other
comments_count: 2
repository_stars: 251886
---

Keep configuration artifacts (ignore rules, dependency wiring, lockfiles) consistent with the real paths/sources used in builds.

Apply:
- **Validate path coverage for globs/ignore rules**: ensure patterns match the actual directory depth.
  - Example: if you need to ignore nested Claude artifacts, don’t rely on a top-level-only pattern.
    ```gitignore
    # Top level
    .claude/*.local.*
    # Also cover nested directories
    compiler/.claude/*.local.*
    ```
- **Stabilize dependency configuration to prevent lockfile drift**: avoid ambiguous or environment-dependent install setups that can change hoisting/resolution.
  - Prefer deterministic local dependency wiring such as `file:` or `link:` over `predev` when that wiring affects which transitive dependencies (and hoisting) you get.
  - Regenerate/commit the affected lockfile entries after fixing the install source configuration.

Result: fewer environment-specific surprises and fewer “regen lock entry” cycles caused by inconsistent config/dependency sources.