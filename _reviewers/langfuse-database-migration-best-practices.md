---
title: Database migration best practices
description: 'When implementing database schema changes, follow these migration best
  practices to maintain data integrity and ensure backward compatibility:


  1. **Create separate migration files** for new schema changes rather than modifying
  existing migrations. This ensures users who already ran previous migrations will
  get new fields added correctly.'
repository: langfuse/langfuse
label: Migrations
language: Sql
comments_count: 3
repository_stars: 13574
---

When implementing database schema changes, follow these migration best practices to maintain data integrity and ensure backward compatibility:

1. **Create separate migration files** for new schema changes rather than modifying existing migrations. This ensures users who already ran previous migrations will get new fields added correctly.

```sql
-- DO NOT add new columns to existing migration files
-- packages/shared/prisma/migrations/20230924232619_datasets_init/migration.sql
CREATE TABLE "dataset_items" (
  /* existing fields */
  "comment" TEXT, -- ❌ Adding here breaks compatibility
);

-- DO create a separate migration file for new columns
-- packages/shared/prisma/migrations/20250607040909_add_comment_to_dataset_items/migration.sql
ALTER TABLE "dataset_items" ADD COLUMN "comment" TEXT; -- ✓ Correct approach
```

2. **Use consistent naming conventions** for migration files to ensure correct execution order. For this project, use 4 leading digits in filenames (e.g., '0011_' not '00011_').

3. **Use database-specific syntax correctly**. For example, with ClickHouse:
   - Include `ON CLUSTER default` for cluster operations
   - Use the precise command for the object type (e.g., `DROP MATERIALIZED VIEW` not `DROP VIEW`)

Following these practices ensures migrations run reliably across all environments and prevents data inconsistencies.