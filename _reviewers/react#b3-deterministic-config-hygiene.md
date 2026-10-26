---
title: Deterministic Config Hygiene
description: 'Treat configuration as part of your build contract: make ignore/config
  patterns accurately cover every generated path, and keep dependency install configuration
  deterministic so lockfiles don’t drift.'
repository: facebook/react#b3
label: Configurations
language: Other
comments_count: 2
repository_stars: 251883
---

Treat configuration as part of your build contract: make ignore/config patterns accurately cover every generated path, and keep dependency install configuration deterministic so lockfiles don’t drift.

Apply:
- Ignore rules: When tooling generates files in subdirectories (e.g., per-package caches), ensure `.gitignore` patterns match those nested paths. Avoid assumptions that a pattern only covers the top level.
  Example pattern:
  ```gitignore
  # Ignore generated Claude local files in any subdir
  .claude/*.local.*
  # If a tool writes under nested locations, cover them explicitly
  compiler/.claude/*.local.*
  ```
- Dependency/install configuration: If your install flow (scripts, workspace setup like `predev`, etc.) can change hoisting/version resolution, prefer deterministic dependency links rather than brittle indirection.
  Example guidance:
  - Prefer `file:` or `link:` protocols over ad-hoc predev/workspace tricks.
  - If the dependency graph changes, regenerate the affected lock entries and commit the update.

Outcome: fewer “it works on my machine” issues, cleaner repos, and stable, compatible configuration-driven builds.