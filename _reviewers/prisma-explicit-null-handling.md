---
title: explicit null handling
description: Prefer explicit null and undefined handling over optional or nullable
  types. When possible, provide default values or objects instead of making parameters
  optional. When null/undefined checks are necessary, handle both values explicitly
  and use descriptive patterns.
repository: prisma/prisma
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 42967
---

Prefer explicit null and undefined handling over optional or nullable types. When possible, provide default values or objects instead of making parameters optional. When null/undefined checks are necessary, handle both values explicitly and use descriptive patterns.

Instead of relying on optional parameters that create chains of conditional access:
```typescript
// Avoid
interface MigrateSetupInput {
  schemaFilter?: MigrateTypes.SchemaFilter
}
// Later: schemaFilter?.['prop'] access

// Prefer
const defaultSchemaFilter = {
  externalTables: [],
  exclude: [],
} satisfies MigrateTypes.SchemaFilter
```

When checking for null/undefined values, be explicit about both:
```typescript
// Handle both null and undefined
if (obj.currentTimeframe == null) {
  return {}
}

// Or check explicitly
if (response.body === null) {
  return reject(new Error('response.body is null'))
}
```

This approach reduces conditional access chains, makes code more predictable, prevents null reference errors, and improves type safety by making the presence or absence of values explicit rather than implicit.