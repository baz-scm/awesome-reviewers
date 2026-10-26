---
title: Document config across environments
description: 'When configuration or behavior differs by environment (OS-specific paths,
  user profile location, or build/rollout variant), documentation must be explicit
  and “forceable.” Always:'
repository: cline/cline#v23
label: Configurations
language: Other
comments_count: 2
repository_stars: 70889
---

When configuration or behavior differs by environment (OS-specific paths, user profile location, or build/rollout variant), documentation must be explicit and “forceable.” Always:

- Provide platform-correct path examples (don’t rely on `~` alone; for Windows, show the equivalent like `%USERPROFILE%`, and avoid ambiguity about which profile type is used).
- When behavior depends on a build/rollout choice, state the exact setting/flag that controls it (and what values do), so users can verify/override rather than guessing.

Example (feature/rollout override):
```json
// VS Code settings (example)
{
  "cline.rollout.bundleOverride": "next"   // or "legacy"; "auto" follows rollout
}
```

Example (path documentation approach):
- Prefer a docs format that lists both Linux/macOS and Windows equivalents for user-scoped plugin directories instead of only `~/...`, so Windows users aren’t blocked by unclear home-directory expansion.