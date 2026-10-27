---
title: Config Consistency Standards
description: 'Ensure configuration-related artifacts are complete and reproducible
  across the paths and install contexts they affect.


  Apply this to both generated local files and dependency/lock configuration:'
repository: facebook/react#b14
label: Configurations
language: Other
comments_count: 2
repository_stars: 251893
---

Ensure configuration-related artifacts are complete and reproducible across the paths and install contexts they affect.

Apply this to both generated local files and dependency/lock configuration:
- Ignore rules: when tooling can write “local” files under nested directories, ensure ignore patterns cover those subpaths (not just the top level). For example:
  - Prefer patterns like `**/.claude/*.local.*` or explicit nested paths such as `compiler/.claude/*.local.*` rather than only `/.claude/*.local.*`.
- Dependency/lock configuration: avoid ambiguous or legacy install mechanisms that can change how Yarn hoists/resolves packages. If you hit incompatibilities (e.g., missing expected transitive deps causing different hoist behavior), regenerate the affected lock entries via a clean install and switch fixture dependency sources to stable protocols such as `file:` or `link:`.

Example gitignore improvement:
```gitignore
# Ignore any tool-local files, including nested generated directories
**/.claude/*.local.*
```

Example dependency source improvement (conceptual):
- Replace custom/legacy “predev” sources with `file:`/`link:` so the fixture installs consistently and the lockfile remains compatible.