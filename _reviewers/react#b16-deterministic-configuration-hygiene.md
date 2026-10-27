---
title: Deterministic Configuration Hygiene
description: Keep configuration changes reproducible and environment-safe by (1) precisely
  ignoring environment/generated artifacts and (2) using deterministic dependency
  sourcing for local packages.
repository: facebook/react#b16
label: Configurations
language: Other
comments_count: 2
repository_stars: 251891
---

Keep configuration changes reproducible and environment-safe by (1) precisely ignoring environment/generated artifacts and (2) using deterministic dependency sourcing for local packages.

Apply it like this:
- Ignore the right paths: ensure ignore patterns cover nested tool output locations (not just top-level directories).
  - Example:
    ```gitignore
    # Tool local data (top-level + nested)
    .claude/*.local.*
    **/.claude/*.local.*
    ```
- Use stable local dependency protocols: prefer `file:` or `link:` for local packages instead of custom install hooks that can alter Yarn’s dependency hoisting.
  - Example (package.json):
    ```json
    {
      "dependencies": {
        "some-local-pkg": "file:../some-local-pkg"
        // or "link:../some-local-pkg"
      }
    }
    ```
- When install/config topology changes, regenerate and commit the lockfile (or the affected entries) to avoid mismatched dependency graphs across environments.