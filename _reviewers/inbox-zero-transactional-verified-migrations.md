---
title: Transactional verified migrations
description: Enhance database migration reliability by wrapping changes in transactions
  with pre-check and post-verification steps. This pattern prevents partial migrations
  that could leave your database in an inconsistent state.
repository: elie222/inbox-zero
label: Migrations
language: Sql
comments_count: 5
repository_stars: 8267
---

Enhance database migration reliability by wrapping changes in transactions with pre-check and post-verification steps. This pattern prevents partial migrations that could leave your database in an inconsistent state.

For any substantial schema change or data migration:

1. Begin with pre-checks to validate assumptions
2. Wrap all operations in a single transaction
3. Include post-operation verification
4. Use defensive SQL patterns (`IF EXISTS` clauses, pre-checks before constraints)

Example of a robust migration pattern:

```sql
BEGIN;

-- Pre-check to validate assumptions
DO $$ 
BEGIN
  IF EXISTS (
    SELECT digestFrequencyId
    FROM "EmailAccount"
    WHERE digestFrequencyId IS NOT NULL
    GROUP BY digestFrequencyId
    HAVING COUNT(*) > 1
  ) THEN
    RAISE EXCEPTION 'Duplicate values found; please resolve before migrating.';
  END IF;
END $$;

-- Safe schema changes with defensive patterns
ALTER TABLE "EmailAccount" DROP CONSTRAINT IF EXISTS "EmailAccount_digestScheduleId_fkey";
DROP INDEX IF EXISTS "EmailAccount_digestScheduleId_key";

-- For NOT NULL constraints, use a two-step approach
ALTER TABLE "CleanupJob" ADD COLUMN "email" TEXT; -- First add as nullable
UPDATE "CleanupJob" SET "email" = 'placeholder@example.com'; -- Backfill data
ALTER TABLE "CleanupJob" ALTER COLUMN "email" SET NOT NULL; -- Then set NOT NULL

-- Post-verification to confirm success
DO $$
BEGIN
  IF EXISTS (
    -- Query to verify migration succeeded as expected
    SELECT 1 FROM "CleanupJob" WHERE "email" IS NULL
  ) THEN
    RAISE EXCEPTION 'Verification failed: nullable emails found';
  END IF;
END $$;

COMMIT;
```

This approach makes migrations safer, more reliable, and helps prevent production incidents from failed or partial migrations.