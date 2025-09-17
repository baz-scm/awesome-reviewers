---
title: Use defensive SQL clauses
description: Always use defensive SQL clauses like `IF NOT EXISTS` and `IF EXISTS`
  in migration scripts to make them idempotent and prevent failures when run multiple
  times or in different environments. This ensures migrations can be safely re-executed
  without causing errors due to existing schema elements.
repository: juspay/hyperswitch
label: Migrations
language: Sql
comments_count: 2
repository_stars: 34028
---

Always use defensive SQL clauses like `IF NOT EXISTS` and `IF EXISTS` in migration scripts to make them idempotent and prevent failures when run multiple times or in different environments. This ensures migrations can be safely re-executed without causing errors due to existing schema elements.

Example:
```sql
-- Good: Uses IF NOT EXISTS to prevent errors
ALTER TABLE payment_intent ADD COLUMN IF NOT EXISTS enable_overcapture BOOLEAN;

-- Good: Uses IF EXISTS for safe removal
ALTER TABLE subscription DROP COLUMN IF EXISTS profile_id;
```

When performing complex operations like column renaming or constraint modifications, understand that some operations require separate statements and cannot be nested within a single ALTER TABLE command.