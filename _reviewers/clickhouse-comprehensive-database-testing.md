---
title: Comprehensive database testing
description: Database tests should verify both query execution and optimization behavior
  through comprehensive scenario coverage. When testing query optimizations, include
  EXPLAIN PLAN verification to ensure the optimizer produces expected execution plans.
  For database features like row policies or security constraints, test multiple scenarios
  including edge cases and...
repository: ClickHouse/ClickHouse
label: Database
language: Sql
comments_count: 2
repository_stars: 42425
---

Database tests should verify both query execution and optimization behavior through comprehensive scenario coverage. When testing query optimizations, include EXPLAIN PLAN verification to ensure the optimizer produces expected execution plans. For database features like row policies or security constraints, test multiple scenarios including edge cases and complex configurations.

Example approach:
```sql
-- Test the actual query execution
SELECT 1
FROM t2
LEFT JOIN t1 ON t2.id = t1.fid
LEFT JOIN t3 ON t1.tid = t3.id
WHERE (t2.resource_id IS NOT NULL) AND (t2.status IN ('OPEN'));

-- Also verify the execution plan
EXPLAIN PLAN
SELECT 1 FROM t2 LEFT JOIN t1 ON t2.id = t1.fid...

-- Test multiple policy scenarios
CREATE ROW POLICY permissive_policy ON table USING condition1;
CREATE ROW POLICY restrictive_policy ON table USING condition2;
-- Test cases where policy columns aren't selected
SELECT other_column FROM table WHERE some_condition;
```

This ensures database functionality works correctly and performs optimally across various real-world scenarios, catching both functional bugs and performance regressions.