---
title: organize related code together
description: Keep related functionality grouped together to improve code discoverability
  and maintainability. This includes placing related functions in the same module,
  maintaining consistent test file placement, and avoiding unnecessary file fragmentation.
repository: remix-run/react-router
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 55270
---

Keep related functionality grouped together to improve code discoverability and maintainability. This includes placing related functions in the same module, maintaining consistent test file placement, and avoiding unnecessary file fragmentation.

Key practices:
- Place related functions near each other (e.g., `prependBasename` should live in `utils.ts` next to `stripBasename`)
- Maintain consistent test file organization within the repository - either always use `__tests__` directories or always place tests next to implementation
- Avoid creating single-line modules when the code could logically belong in an existing utility module
- Group related types and exports in appropriate directory structures (e.g., exports from `internal-export.ts` live in `types/internal-export/` folder)
- Prefer direct imports from source files over barrel file re-exports to maintain clear dependency relationships

Example of good organization:
```typescript
// utils.ts - related string manipulation functions together
export function stripBasename(pathname: string, basename: string) { ... }
export function prependBasename(pathname: string, basename: string) { ... }

// Avoid creating separate single-line modules when functionality fits logically elsewhere
// Instead of: types/register.ts with just "export interface Register {}"
// Consider: utils.ts or existing appropriate module
```

This approach reduces cognitive load when navigating the codebase and makes it easier to find related functionality.