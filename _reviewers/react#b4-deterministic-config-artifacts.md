---
title: Deterministic Config Artifacts
description: 'When adding/using configuration-related generated files or local dependency
  wiring, ensure the repo stays deterministic:


  - Scope ignores to the *actual* directories where config artifacts are created (including
  nested paths). Prefer patterns that cover both top-level and subdirectories.'
repository: facebook/react#b4
label: Configurations
language: Other
comments_count: 2
repository_stars: 251885
---

When adding/using configuration-related generated files or local dependency wiring, ensure the repo stays deterministic:

- Scope ignores to the *actual* directories where config artifacts are created (including nested paths). Prefer patterns that cover both top-level and subdirectories.
- Avoid custom local install flows that change dependency hoisting/resolution unexpectedly; prefer deterministic protocols like `file:` or `link:` for local packages.
- After switching protocols or resolving dependency graph changes, regenerate/update the relevant lockfile entries (don’t rely on stale resolutions).

Example (.gitignore) pattern approach:
```gitignore
# Ignore Claude-generated local artifacts across nested project areas
.claude/*.local.*
compiler/.claude/*.local.*
# or a single broader glob if appropriate for your tree
# **/.claude/*.local.*
```

Example (Yarn local dependency wiring):
- Prefer `file:`/`link:` in your manifest/workspaces for local packages over an ad-hoc `predev` install step, then run `yarn install` and update `yarn.lock` to reflect the new deterministic resolution.