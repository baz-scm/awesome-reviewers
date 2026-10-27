---
title: Reproducible config hygiene
description: 'Ensure configuration-related artifacts and dependency inputs are handled
  deterministically across the repo.


  - Ignore local/generated configuration files everywhere they may appear (including
  nested packages). Use path patterns that cover subdirectories, not just the repo
  root.'
repository: facebook/react#b7
label: Configurations
language: Other
comments_count: 2
repository_stars: 251888
---

Ensure configuration-related artifacts and dependency inputs are handled deterministically across the repo.

- Ignore local/generated configuration files everywhere they may appear (including nested packages). Use path patterns that cover subdirectories, not just the repo root.
  - Example: instead of only ignoring top-level `/.claude`, ignore nested variants too (e.g., `**/.claude/*.local.*`).

- Keep dependency resolution stable for fixtures and local installs by avoiding dev tooling/protocols that cause Yarn to re-hoist or otherwise change the dependency graph unexpectedly.
  - Prefer explicit `file:` or `link:` protocols over indirection like `predev`.
  - When the dependency graph changes due to configuration/input changes, regenerate the affected lockfile(s) in that fixture scope and commit the updated results.

This prevents accidental commits of local config state and reduces surprise lockfile churn caused by non-reproducible install paths.