---
title: Validate configuration paths
description: When updating configuration docs or build/package behavior, ensure (a)
  any filesystem paths are correct for every supported OS/profile style, and (b) ignore/include
  rules actually match the behavior of the underlying tooling.
repository: cline/cline#v16
label: Configurations
language: Other
comments_count: 2
repository_stars: 70882
---

When updating configuration docs or build/package behavior, ensure (a) any filesystem paths are correct for every supported OS/profile style, and (b) ignore/include rules actually match the behavior of the underlying tooling.

Apply this as a checklist:
- **Path correctness:** If you document or use `~`/home-dir paths, confirm what it expands to on each OS (e.g., Windows `~` vs `%USERPROFILE%`, and whether the relevant profile type is supported). Prefer explicit, cross-platform forms when possible.
- **Config truthfulness:** Don’t add redundant ignore rules that the build tool already enforces. Instead, verify behavior with the tool itself (e.g., list what would be packaged) and keep configuration minimal and accurate.

Example (explicit home/profile usage in docs or scripts):
```sh
# Prefer explicit env vars over ambiguous ~ when supporting multiple OSes.
# Windows: %USERPROFILE% ; POSIX: $HOME
GLOBAL_PLUGINS_DIR="${USERPROFILE:-$HOME}/.cline/plugins"
PROJECT_PLUGINS_DIR="$(pwd)/.cline/plugins"
USER_DOC_PLUGINS_DIR="${USERPROFILE:-$HOME}/Documents/Cline/Plugins"
```

Example (validation approach for packaging rules):
- After changing ignore/include config, run a packaging “list” command (or an equivalent deterministic check) and confirm the files you expect are present/absent, rather than assuming the effective rules from duplicates.