---
title: Config Documentation Must Be Precise
description: When writing or updating configuration-related documentation (paths,
  generated files, feature flags/rollouts), ensure the doc is unambiguous and matches
  real runtime behavior across environments.
repository: cline/cline#v25
label: Configurations
language: Other
comments_count: 3
repository_stars: 70891
---

When writing or updating configuration-related documentation (paths, generated files, feature flags/rollouts), ensure the doc is unambiguous and matches real runtime behavior across environments.

Apply these rules:
1. **Avoid ambiguous home/path shortcuts**: If the product uses `~`, ensure the documentation also states the effective equivalent on major platforms (e.g., Windows user profile) or uses explicit OS-appropriate paths.
2. **Ignore generated config artifacts correctly**: If your app writes config/state into workspace subfolders, use ignore rules that actually match nested locations, and validate them (e.g., with `git check-ignore`).
3. **Document the controlling config knobs**: If behavior varies by rollout/build/loader, name the exact settings key(s) and how to force a variant (and what `auto` does).

Example (ignore patterns for nested enterprise config state):
```text
# Works even when the workspace is nested/opened in a subfolder
**/.cline/enterprise/
**/.cline/remote-config/
```
Example (feature rollout override):
```json
// VS Code settings: force which auto-approve implementation is used
"cline.rollout.bundleOverride": "next" // or "legacy"
// "auto" follows the rollout
```