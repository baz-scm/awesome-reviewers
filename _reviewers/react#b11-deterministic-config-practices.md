---
title: Deterministic Config Practices
description: Ensure configuration-driven behavior is both comprehensive (covers every
  relevant path/scope) and deterministic (dependency sourcing doesn’t change behavior
  via hoisting or environment-specific setups).
repository: facebook/react#b11
label: Configurations
language: Other
comments_count: 2
repository_stars: 251894
---

Ensure configuration-driven behavior is both comprehensive (covers every relevant path/scope) and deterministic (dependency sourcing doesn’t change behavior via hoisting or environment-specific setups).

Apply:
- Config file patterns: don’t assume top-level anchors cover nested directories. Verify patterns match real locations.
  - Example (.gitignore):
    ```gitignore
    .claude/*.local.*
    ./compiler/.claude/*.local.*
    ```
- Dependency configuration: prefer explicit, stable protocols for local packages and keep lockfiles consistent with the resulting install graph.
  - Example (conceptual): replace a brittle/ambiguous `predev` approach with `file:` or `link:` sources, then regenerate the lockfile so the resolved versions are reproducible.

If you change how files are produced/consumed (ignore rules) or how packages are resolved (local dependency protocols), update the relevant config/lockfile together to prevent subtle environment-specific breakage.