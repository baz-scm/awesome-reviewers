---
title: Define schema relations correctly
description: 'When designing database schemas, ensure relations and constraints are
  explicitly and correctly defined:


  1. Every model must have a properly defined primary key:'
repository: elie222/inbox-zero
label: Database
language: Prisma
comments_count: 4
repository_stars: 8267
---

When designing database schemas, ensure relations and constraints are explicitly and correctly defined:

1. Every model must have a properly defined primary key:
```prisma
model EmailAccount {
  email String @id  // Primary key, not just @unique
  // OR
  id String @id @default(cuid())  // UUID as primary key
  email String @unique  // Unique but not primary key
}
```

2. Always use explicit @relation directives with field references:
```prisma
model EmailAccount {
  accountId String @unique
  account Account @relation(fields: [accountId], references: [id])
}
```

3. Avoid redundant foreign keys that Prisma implicitly manages:
```diff
-  digestSchedule Schedule?
-  digestScheduleId String? @unique
+  digestSchedule Schedule? // Let Prisma handle the relation
```

4. Carefully evaluate unique constraints to ensure they won't restrict valid use cases:
```prisma
// ❌ Too restrictive - prevents multiple actions of same type
@@unique([executedRuleId, actionType])

// ✅ Better - includes distinguishing field
@@unique([executedRuleId, actionType, targetIdentifier])
```

Proper relation definitions improve schema clarity, prevent migration issues, and avoid runtime errors from phantom fields or missing constraints.