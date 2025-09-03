---
title: Optimize database column types
description: Choose appropriate data types for database columns to improve storage
  efficiency and performance. Use auto-incrementing identity columns for primary keys
  when there are no specific semantic requirements, and select column types with proper
  constraints based on expected data characteristics.
repository: lobehub/lobe-chat
label: Database
language: TypeScript
comments_count: 3
repository_stars: 65138
---

Choose appropriate data types for database columns to improve storage efficiency and performance. Use auto-incrementing identity columns for primary keys when there are no specific semantic requirements, and select column types with proper constraints based on expected data characteristics.

For primary keys without semantic meaning, prefer identity columns over text-based custom IDs:

```ts
// Preferred: Auto-incrementing identity
id: integer('id').primaryKey().generatedByDefaultAsIdentity(),

// Avoid: Custom text-based IDs when not semantically required
id: text('id').$defaultFn(() => idGenerator('usageRecords', 16)).primaryKey(),
```

For string columns, use varchar with appropriate length constraints instead of unbounded text types:

```ts
// Preferred: Constrained varchar for better storage
callType: varchar('call_type', { length: 256 }).notNull(),

// Avoid: Text with enum configuration when varchar suffices
callType: text('call_type', { enum: ['chat', 'history_summary'] }).notNull(),
```

This approach reduces storage overhead, improves query performance, and provides better data validation at the database level.