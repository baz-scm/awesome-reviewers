---
title: Consistent clear naming
description: Use consistent terminology across similar concepts and choose names that
  clearly indicate their purpose. Avoid overloaded terms that cause confusion in your
  domain context, and ensure naming conventions align with established patterns.
repository: prisma/prisma
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 42967
---

Use consistent terminology across similar concepts and choose names that clearly indicate their purpose. Avoid overloaded terms that cause confusion in your domain context, and ensure naming conventions align with established patterns.

Key principles:
- **Consistency across similar concepts**: Use the same naming pattern for related functionality (e.g., "Driver Adapters" not "Prisma Adapters")
- **Avoid overloaded terms**: When a term has multiple meanings in your domain, use aliases or more specific names (e.g., alias `Schema` import as `Shape` to avoid confusion with domain Schema)
- **Clear purpose indication**: Choose names that make functionality obvious and discoverable to users (e.g., `ignoreSpanNames` instead of `ignoreLayersTypes` when filtering spans)
- **Domain-appropriate terminology**: Use terminology that matches the domain or external standards you're working with

Example of good naming consistency:
```typescript
// Good - consistent naming across adapters
export class DriverAdapterError extends Error {
  name = 'DriverAdapterError'
}

// Bad - inconsistent terminology
export class PrismaAdapterError extends Error {
  name = 'PrismaAdapterError'  
}
```

Example of avoiding overloaded terms:
```typescript
// Good - avoids confusion with domain Schema
import { Schema as Shape } from 'effect'

// Potentially confusing in Prisma context
import { Schema } from 'effect'
```