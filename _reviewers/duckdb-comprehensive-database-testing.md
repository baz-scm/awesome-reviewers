---
title: comprehensive database testing
description: Database tests should execute actual queries and verify results comprehensively,
  not just check query plans or use hash comparisons. Always include edge cases, test
  data scenarios with both expected and unexpected data, and verify storage correctness
  through restart/reload cycles.
repository: duckdb/duckdb
label: Database
language: Other
comments_count: 4
repository_stars: 32061
---

Database tests should execute actual queries and verify results comprehensively, not just check query plans or use hash comparisons. Always include edge cases, test data scenarios with both expected and unexpected data, and verify storage correctness through restart/reload cycles.

Key practices:
- Execute queries and verify actual results rather than only checking query plans
- Use labeled results with `nosort` instead of hash comparisons for result verification
- Add comprehensive test cases covering edge cases, null/non-null data, and boundary conditions
- For storage tests, include restart/reload verification to ensure data persistence correctness
- Test both positive cases (expected data) and negative cases (edge conditions)

Example of proper test verification:
```sql
query III nosort read_csv_result
SELECT * FROM read_csv('test/data.csv') WITH ORDINALITY ORDER BY col1, col2, ordinality;

query III nosort read_csv_result  
SELECT *, row_number() OVER () AS ordinality FROM read_csv('test/data.csv') ORDER BY col1, col2, ordinality;
```

For storage tests, always verify data integrity after database restart:
```sql
statement ok
CREATE TABLE test_table AS SELECT * FROM large_dataset;

# Restart database
restart

query I
SELECT COUNT(*) FROM test_table;
```

This approach ensures database functionality works correctly under real-world conditions and catches issues that plan-only testing might miss.