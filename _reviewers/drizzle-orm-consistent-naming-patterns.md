---
title: consistent naming patterns
description: Maintain consistent naming conventions across similar constructs in your
  codebase. This includes using consistent prefixes for related methods and following
  established patterns for file imports and extensions.
repository: drizzle-team/drizzle-orm
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 29461
---

Maintain consistent naming conventions across similar constructs in your codebase. This includes using consistent prefixes for related methods and following established patterns for file imports and extensions.

When you have similar methods or functions that perform related operations, use consistent naming patterns. For example, if you have a `createJoin` method, related methods should follow the same pattern like `createSetOperator` rather than just `setOperator`.

Similarly, maintain consistency in file import conventions. If your project uses explicit file extensions in imports, apply this pattern consistently across all imports.

Example of consistent method naming:
```typescript
// Good - consistent "create" prefix
private createJoin(...)
private createSetOperator(...)

// Inconsistent - mixed naming patterns  
private createJoin(...)
private setOperator(...)
```

Example of consistent import conventions:
```typescript
// Good - consistent .ts extensions
import type { ColumnBaseConfig } from '~/column.ts';
import { entityKind } from '~/entity.ts';

// Inconsistent - missing extension
import type { ColumnBaseConfig } from '~/column';
```

Consistent naming patterns improve code readability, reduce cognitive load for developers, and make the codebase easier to navigate and maintain.