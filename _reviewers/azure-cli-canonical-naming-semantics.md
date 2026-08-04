---
title: Canonical naming semantics
description: When configuring or referencing named entities, use the *canonical identifier*
  required by the consuming system and ensure the identifier’s *semantic type* matches
  what the field expects (e.g., “team” vs “label”). If a system normalizes names,
  reference the normalized form—not the on-disk/path form—and don’t substitute a label
  for a team.
repository: Azure/azure-cli
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 4592
---

When configuring or referencing named entities, use the *canonical identifier* required by the consuming system and ensure the identifier’s *semantic type* matches what the field expects (e.g., “team” vs “label”). If a system normalizes names, reference the normalized form—not the on-disk/path form—and don’t substitute a label for a team.

Examples:
- External system normalization (Homebrew tap): if your repo is named `dev/homebrew-azure-cli`, Homebrew refers to it as `dev/azure-cli`. Use the normalized tap name when writing commands/configs (and don’t assume the prefix is part of the logical identifier).
- Semantic type correctness (policy mentionees): if a field expects team names, replace label-like identifiers with the correct team value.

Practical checks:
- For any identifier used in CI/tooling/config, confirm the system’s “logical” name (docs or prior working examples) vs the local repo/path name.
- For any structured field (like `mentionees`), confirm the expected entity type. If it’s “team”, don’t provide label strings.
- Add a short comment documenting any necessary mapping (e.g., “on disk vs logical tap name”).