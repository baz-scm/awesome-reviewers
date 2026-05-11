---
title: Consistent Unique Package Names
description: 'Use stable naming conventions that match repo/tooling expectations and
  avoid identifier collisions.


  **Rules**

  1. **Keep script names consistent across packages**: if CI/tooling expects specific
  npm/pnpm script keys, use the same keys in every package (don’t rename per-package).'
repository: tanstack/query
label: Naming Conventions
language: Json
comments_count: 3
repository_stars: 49380
---

Use stable naming conventions that match repo/tooling expectations and avoid identifier collisions.

**Rules**
1. **Keep script names consistent across packages**: if CI/tooling expects specific npm/pnpm script keys, use the same keys in every package (don’t rename per-package).
2. **Ensure package/example names are globally unique**: every published/package identifier (e.g., `package.json#name`) must be unique across the repo to prevent collisions.
3. **Name compatibility boundaries explicitly**: when an experimental change affects behavior, reflect compatibility intent in naming (e.g., expose a `*-core` for the breaking surface and a separate `*` wrapper that preserves older behavior), instead of changing semantics under the same name.

**Example (package.json)**
```json
{
  "name": "@tanstack/lit-query", 
  "type": "module",
  "scripts": {
    "test:types": "tsc --noEmit",
    "typecheck": "pnpm run test:types",
    "build": "pnpm run build:deps && pnpm run build:esm && pnpm run build:cjs"
  }
}
```
And if you need a compatibility wrapper vs breaking core:
- `@scope/lib-core` (breaking)
- `@scope/lib` (wrapper preserving old behavior)

This prevents CI from skipping packages, avoids naming collisions, and makes breaking/compatibility intent obvious from identifiers.