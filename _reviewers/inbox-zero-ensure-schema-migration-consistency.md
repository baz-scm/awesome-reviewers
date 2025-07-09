---
title: Ensure schema-migration consistency
description: When modifying database schemas, ensure complete alignment between schema
  definitions and SQL migration scripts. Every field, column, constraint, or relationship
  defined in your schema must have a corresponding migration operation.
repository: elie222/inbox-zero
label: Migrations
language: Prisma
comments_count: 2
repository_stars: 8267
---

When modifying database schemas, ensure complete alignment between schema definitions and SQL migration scripts. Every field, column, constraint, or relationship defined in your schema must have a corresponding migration operation.

Common issues to avoid:
- Adding fields to schema models without corresponding `ADD COLUMN` statements in migrations
- Changing field attributes without updating migration constraints
- Forgetting to add columns before defining foreign keys that reference them

Example of problematic changes:
```prisma
// Schema changes:
model EmailAccount {
-  id           String   @id @default(cuid())
+  email        String   @id
   writingStyle String?
+  userId       String
+  accountId    String   @unique
}
```

Without matching migration statements:
```sql
-- Missing corresponding SQL operations:
-- ADD COLUMN "writingStyle" TEXT
-- ADD COLUMN "userId" TEXT NOT NULL
-- ADD COLUMN "accountId" TEXT NOT NULL UNIQUE
```

Failing to maintain this consistency will cause migration failures at runtime. Always verify that every schema field change has a matching migration operation before submitting your PR.