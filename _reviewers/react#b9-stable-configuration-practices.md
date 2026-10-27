---
title: Stable Configuration Practices
description: Ensure configuration-related files (like ignore patterns and dependency
  lockfiles) are deterministic and correctly scoped to the real filesystem and install
  flow.
repository: facebook/react#b9
label: Configurations
language: Other
comments_count: 2
repository_stars: 251891
---

Ensure configuration-related files (like ignore patterns and dependency lockfiles) are deterministic and correctly scoped to the real filesystem and install flow.

Apply this:
- Validate ignore globs against actual paths (don’t assume top-level matches nested dirs). If tooling outputs files in multiple directories, cover both root and nested locations.
  - Example:
    ```gitignore
    # Ignore local Claude artifacts anywhere under .claude
    .claude/*.local.*
    compiler/.claude/*.local.*
    ```
- Use reproducible dependency configuration so lockfiles aren’t reshaped by incompatible hoisting/installation behavior.
  - Prefer stable, standard protocols for local workspace deps (e.g., `file:` or `link:`) instead of custom install flows that can change dependency resolution.
  - If the dependency graph/version changes, regenerate and commit the affected lockfile entries rather than letting inconsistent installs drift.

Result: fewer “it only breaks on my machine” configuration issues and fewer noisy diffs from nondeterministic installs.