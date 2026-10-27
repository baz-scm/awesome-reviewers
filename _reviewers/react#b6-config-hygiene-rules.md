---
title: Config hygiene rules
description: 'When configuration affects environment-specific artifacts (tool outputs,
  local clones, fixture installs), make it exact and deterministic:


  1) Keep ignore/config patterns aligned with real paths'
repository: facebook/react#b6
label: Configurations
language: Other
comments_count: 2
repository_stars: 251888
---

When configuration affects environment-specific artifacts (tool outputs, local clones, fixture installs), make it exact and deterministic:

1) Keep ignore/config patterns aligned with real paths
- Don’t rely on top-level-anchored patterns when generated files can appear in nested tool directories.
- Prefer glob patterns that cover the full directory tree.

Example (`.gitignore`):
```gitignore
# Ignore Claude local tool artifacts anywhere in the repo
**/.claude/*.local.*
```

2) Keep dependency/config installs reproducible
- If a config/installation approach changes how dependencies resolve (e.g., local protocol, predev scripts), regenerate the lockfile and commit the updated `yarn.lock`.
- Avoid installation methods that trigger incompatible hoisting; prefer deterministic local dependency protocols.

Example (guideline):
- Prefer `file:` / `link:` for local packages/fixtures instead of `predev`, and then update/commit the resulting lockfile changes (don’t manually patch stale entries).