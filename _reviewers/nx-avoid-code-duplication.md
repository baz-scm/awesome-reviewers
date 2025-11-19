---
title: Avoid code duplication
description: Before implementing new functionality, check if similar utilities or
  patterns already exist in the codebase. Reuse existing code rather than duplicating
  logic, and organize shared types and constants in centralized locations to prevent
  circular dependencies and maintain consistency.
repository: nrwl/nx
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 27518
---

Before implementing new functionality, check if similar utilities or patterns already exist in the codebase. Reuse existing code rather than duplicating logic, and organize shared types and constants in centralized locations to prevent circular dependencies and maintain consistency.

Key practices:
- Search for existing utilities before creating new ones (e.g., "There is already a `isPrerelease` utility in `packages/nx/src/command-line/release/utils/shared.ts`, let's not duplicate the logic")
- Extract shared types to common files to avoid circular dependencies
- Use generic patterns instead of creating multiple similar functions
- Remove unused variables and unnecessary abstractions

Example of good practice:
```typescript
// Instead of creating multiple similar selectors
export function getMigrationType(ctx: AutomaticMigrationState, migrationId: string) {
  return ctx.nxConsoleMetadata?.completedMigrations?.[migrationId]?.type;
}

// Then use it in components with comparison
const isSuccessful = getMigrationType(ctx, id) === 'successful';
const isFailed = getMigrationType(ctx, id) === 'failed';
```

This approach reduces code duplication, improves maintainability, and ensures consistent behavior across the codebase.