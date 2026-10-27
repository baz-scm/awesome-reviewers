---
title: Deterministic Config Hygiene
description: When changing configuration-related files (including repo ignore rules
  and dependency install configuration), ensure (1) generated environment artifacts
  are comprehensively ignored across all relevant paths, and (2) dependency resolution
  is deterministic so dev-specific install steps don’t cause lockfile drift or incompatible
  hoisting.
repository: facebook/react#b10
label: Configurations
language: Other
comments_count: 2
repository_stars: 251894
---

When changing configuration-related files (including repo ignore rules and dependency install configuration), ensure (1) generated environment artifacts are comprehensively ignored across all relevant paths, and (2) dependency resolution is deterministic so dev-specific install steps don’t cause lockfile drift or incompatible hoisting.

**1) Make ignore patterns cover nested config dirs**
- Don’t rely on top-level globs when generated files can appear under subprojects.

Example:
```gitignore
# Ignore Claude local artifacts anywhere in the repo
.claude/*.local.*
compiler/.claude/*.local.*
```

**2) Prefer stable local dependency protocols and update lockfiles**
- If an install workflow (e.g., a custom `predev` step) leads to Yarn hoisting incompatible dependency versions, switch to deterministic local dependency mechanisms and regenerate the lockfile.

Example (conceptual):
- Replace non-deterministic local setup with `file:` or `link:`-based dependencies, then run `yarn install` and commit the resulting `yarn.lock`.

This prevents accidental commits of environment-generated files and avoids configuration-dependent dependency breakages.