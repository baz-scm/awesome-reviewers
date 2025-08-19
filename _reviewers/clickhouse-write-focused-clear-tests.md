---
title: Write focused, clear tests
description: Tests should be simple, focused on a single concern, and easy to understand.
  When a test combines multiple potential failure conditions or verification points,
  split it into separate, focused test cases. Avoid over-engineering tests with unnecessary
  complexity.
repository: ClickHouse/ClickHouse
label: Testing
language: Sql
comments_count: 2
repository_stars: 42425
---

Tests should be simple, focused on a single concern, and easy to understand. When a test combines multiple potential failure conditions or verification points, split it into separate, focused test cases. Avoid over-engineering tests with unnecessary complexity.

For example, instead of testing multiple failure conditions in one test:
```sql
-- Bad: Unclear which aspect causes failure
CREATE TABLE codecTest (c0 LowCardinality(Nullable(Time)) CODEC(DoubleDelta)) ENGINE = MergeTree() ORDER BY tuple(); -- { serverError BAD_ARGUMENTS }
```

Split into focused tests:
```sql
-- Good: Each test focuses on one specific failure condition
CREATE TABLE codecTest (c0 Time CODEC(DoubleDelta)) ENGINE = MergeTree() ORDER BY tuple(); -- { serverError BAD_ARGUMENTS }
CREATE TABLE codecTest (c0 LowCardinality(String) CODEC(DoubleDelta)) ENGINE = MergeTree() ORDER BY tuple(); -- { serverError BAD_ARGUMENTS }
CREATE TABLE codecTest (c0 Nullable(Int32) CODEC(DoubleDelta)) ENGINE = MergeTree() ORDER BY tuple(); -- { serverError BAD_ARGUMENTS }
```

Similarly, simplify tests that verify basic functionality rather than adding unnecessary verification layers. If the goal is to test that queries don't crash, simple SELECT statements are sufficient without complex EXPLAIN PLAN analysis.