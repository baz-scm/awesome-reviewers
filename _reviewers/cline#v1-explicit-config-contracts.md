---
title: Explicit Config Contracts
description: 'When behavior or deliverables vary by environment/build/rollout, treat
  configuration as an explicit contract: document the exact config keys and values
  users can set, and verify that packaging/ignore configuration matches the tooling’s
  real defaults (removing redundant rules after confirmation).'
repository: cline/cline#v1
label: Configurations
language: Other
comments_count: 2
repository_stars: 70862
---

When behavior or deliverables vary by environment/build/rollout, treat configuration as an explicit contract: document the exact config keys and values users can set, and verify that packaging/ignore configuration matches the tooling’s real defaults (removing redundant rules after confirmation).

How to apply:
- Docs for variant behavior: If runtime behavior changes by build/channel, name the determining setting/flag and the exact values (and note any rollout/autoselection behavior).
- Provide explicit overrides: Prefer a single, discoverable override (e.g., `bundleOverride`) with clear allowed values; ensure documentation doesn’t leave some user cohorts (e.g., nightly) with silently wrong instructions.
- Validate packaging config: Before adding ignore entries, confirm the packaging tool already excludes the artifact class (e.g., `vsce` excluding `**/*.vsix`). Avoid redundant ignore rules and ensure stale files can’t enter the package.

Example (docs for build variants):
```json
// VS Code settings
"cline.rollout.bundleOverride": "next"   // or "legacy"
// "auto" follows rollout
```