---
title: generate test data dynamically
description: Instead of adding static test data files to the repository, generate
  test data programmatically within test cases. This approach improves test modularity,
  reduces repository bloat, and ensures tests are self-contained. Use temporary directories
  for any files that need to be written during testing.
repository: duckdb/duckdb
label: Testing
language: Csv
comments_count: 3
repository_stars: 32061
---

Instead of adding static test data files to the repository, generate test data programmatically within test cases. This approach improves test modularity, reduces repository bloat, and ensures tests are self-contained. Use temporary directories for any files that need to be written during testing.

When you need test data, create it using code rather than committing large CSV files or other data files. For example:

```sql
statement ok
CREATE TABLE my_tbl (a int, b int, c varchar);

statement ok
INSERT INTO my_tbl SELECT range, 5000 - range, 'cooler string' FROM range(5000);

statement ok
COPY tbl TO '__TEST_DIR__/output.csv' (HEADER, DELIMITER ',');
```

This keeps tests modular, avoids persistent files between test runs, and makes the test data generation explicit and maintainable within the test itself.