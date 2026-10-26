---
title: Configuration documentation precision
description: When documenting or implementing configuration, be explicit and deterministic
  about (1) path semantics across platforms, (2) where workspace-generated configuration/caches
  are written and how to keep them out of version control, and (3) which config/flag
  selects behavior when multiple builds/rollouts are present.
repository: cline/cline#v11
label: Configurations
language: Other
comments_count: 3
repository_stars: 70871
---

When documenting or implementing configuration, be explicit and deterministic about (1) path semantics across platforms, (2) where workspace-generated configuration/caches are written and how to keep them out of version control, and (3) which config/flag selects behavior when multiple builds/rollouts are present.

Apply this checklist:
- **Don’t leave path meaning ambiguous.** If you use `~`, confirm it resolves correctly on Windows user profiles and roaming/non-roaming scenarios; otherwise provide Windows-equivalent guidance (e.g., `%USERPROFILE%`) or use explicit, OS-aware paths.
- **Specify exact workspace output folders and safe repo hygiene.** For any tool that writes cached/derived config into the repo workspace, document the folder names and add `.gitignore` patterns that match nested locations.
- **Document the exact controlling flag and mapping to behavior.** If two builds/loaders exist (legacy/next, SDK-based vs prior), state which setting deterministically selects each behavior and how the UI/behavior differs.

Example (.gitignore for nested cached config):
```text
# Workspace-generated enterprise/remote config (may contain secrets)
**/.cline/enterprise/
**/.cline/remote-config/
```

Example (explicit rollout override):
```text
# VS Code setting
cline.rollout.bundleOverride = next   # or legacy
# auto follows rollout
```