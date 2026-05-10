---
title: Consistent Scoped Naming
description: 'Use consistent, semantic naming patterns for externally visible identifiers—especially
  package names and command/script names.


  - **Packages/registry entries:** Prefer the correct scope and canonical name format
  (typically `@scope/name`) aligned with ownership and established ecosystem conventions.
  If the project belongs under a scope (e.g., `@zod`), use...'
repository: colinhacks/zod
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 42628
---

Use consistent, semantic naming patterns for externally visible identifiers—especially package names and command/script names.

- **Packages/registry entries:** Prefer the correct scope and canonical name format (typically `@scope/name`) aligned with ownership and established ecosystem conventions. If the project belongs under a scope (e.g., `@zod`), use `@zod/zod`-style naming rather than an unrelated owner-scope.
  - Example: change a JSR `name` to `@zod/zod` (or equivalent `@zod/*`) instead of keeping an `@colinhacks/*` identity when ownership/pattern indicates `@zod/*`.

- **Grouped scripts/commands:** When defining related commands, use a consistent hierarchy delimiter such as `:` to make relationships obvious.
  - Example:
    ```json
    {
      "scripts": {
        "fix:lint": "eslint --fix --ext .ts ./src",
        "fix:format": "prettier --write \"src/**/*.ts\"",
        "fix": "yarn fix:lint && yarn fix:format"
      }
    }
    ```