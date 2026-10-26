---
title: Deterministic Config Hygiene
description: 'Make configuration changes precise and reproducible across environments/fixtures.


  - For config/tool-generated local files: ensure ignore (and other config path patterns)
  cover all relevant directory depths, not just top-level folders. For example, instead
  of a pattern that only matches `/.claude`, use a recursive glob so nested tool directories
  are also...'
repository: facebook/react#b1
label: Configurations
language: Other
comments_count: 2
repository_stars: 251878
---

Make configuration changes precise and reproducible across environments/fixtures.

- For config/tool-generated local files: ensure ignore (and other config path patterns) cover all relevant directory depths, not just top-level folders. For example, instead of a pattern that only matches `/.claude`, use a recursive glob so nested tool directories are also ignored:
  ```gitignore
  # Ignore Claude local artifacts at any depth
  **/.claude/*.local.*
  ```
- For fixture dependency configuration (lockfiles/install wiring): avoid install-protocol indirections that lead to inconsistent dependency hoisting/resolution. If a workspace/fixture setup causes incompatible transitive deps, regenerate the affected lock entries and prefer deterministic protocols like `file:` or `link:` over ambiguous `predev`-style setups.
  - After changing install inputs/protocols, run an install and commit the resulting lockfile updates so the fixture remains reproducible.