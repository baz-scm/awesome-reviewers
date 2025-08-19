---
title: comprehensive test coverage
description: Ensure thorough test coverage by systematically testing edge cases, boundary
  conditions, failure scenarios, and different data types. When implementing new functionality,
  consider all possible input variations, error conditions, and integration points.
repository: duckdb/duckdb
label: Testing
language: Other
comments_count: 7
repository_stars: 32061
---

Ensure thorough test coverage by systematically testing edge cases, boundary conditions, failure scenarios, and different data types. When implementing new functionality, consider all possible input variations, error conditions, and integration points.

Key areas to cover:
- **Boundary values**: Test minimum, maximum, and overflow conditions for numeric types
- **Edge cases**: Empty inputs, null values, special characters, and unusual data patterns
- **Failure conditions**: Invalid inputs, type mismatches, and error scenarios
- **Data type variations**: Test across different compatible types and type conversions
- **Integration scenarios**: Test interactions with related features and nested operations

Use systematic approaches like foreach loops to ensure comprehensive coverage:

```sql
foreach type <integral> varchar
query T
SELECT list_contains([1,2,3], $1::$2)
----
# expected results
endloop
```

Examples of comprehensive test cases:
- For hex parsing: test empty hex (`'0x'::INT`), case variations (`'0XFF'::INT`), overflow conditions (`'0xFFFFFFFFFFFFFFFFF'::INT`), and exact boundary values
- For string operations: test strings longer than 12 characters (handled differently in DuckDB)
- For null handling: test null inputs, null in collections, and null propagation
- For new parameters: test across related features (e.g., if implementing for Parquet, also test for CSV)

This approach helps achieve near 100% code coverage and prevents regression issues by thoroughly exercising all code paths.