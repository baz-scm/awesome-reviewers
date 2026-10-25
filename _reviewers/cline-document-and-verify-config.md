---
title: Document and Verify Config
description: For any feature flags/rollout settings or build/packaging configuration
  that affects runtime behavior, ensure (1) the docs accurately describe the exact
  config key, supported values, and override/rollout semantics, and (2) packaging/ignore
  rules are verified against the actual tool/script defaults so you don’t keep stale
  or redundant entries.
repository: cline/CLINE
label: Configurations
language: Other
comments_count: 2
repository_stars: 70839
---

For any feature flags/rollout settings or build/packaging configuration that affects runtime behavior, ensure (1) the docs accurately describe the exact config key, supported values, and override/rollout semantics, and (2) packaging/ignore rules are verified against the actual tool/script defaults so you don’t keep stale or redundant entries.

Apply it like this:
- Feature-flag/docs
  - Use the real setting key and explain what each value does, including how `auto` differs from explicit overrides.
  - Keep docs in sync with how the code derives or applies the config.

  Example (VS Code settings override documentation):
  ```json
  // Explicit override
  {
    "cline.rollout.bundleOverride": "next"   // or "legacy"
  }
  // Leaving it as "auto" (or unset) follows rollout selection.
  ```
- Packaging/ignore config
  - When changing `.vscodeignore`/ignore lists, verify which files are actually included/excluded by `vsce` and any custom packaging scripts.
  - Remove redundant ignore lines that merely repeat tool defaults, to reduce future drift.

Acceptance checks:
- A maintainer should be able to set/understand the correct configuration without reading code.
- A packaging dry-run (or equivalent command) should confirm the effective artifact contents match the intended ignore/include behavior.