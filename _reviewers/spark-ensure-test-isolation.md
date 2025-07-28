---
title: ensure test isolation
description: Tests must properly clean up resources and avoid side effects that can
  impact other tests, especially when running in parallel. This prevents non-deterministic
  failures and ensures reliable test execution.
repository: apache/spark
label: Testing
language: Python
comments_count: 2
repository_stars: 41554
---

Tests must properly clean up resources and avoid side effects that can impact other tests, especially when running in parallel. This prevents non-deterministic failures and ensures reliable test execution.

Key practices:
- Clean up any created resources (tables, files, connections) after test completion
- Use unique identifiers for test resources to avoid conflicts
- Ensure tests don't leave persistent state that affects subsequent tests
- Consider using test fixtures or teardown methods for consistent cleanup

Example of proper cleanup:
```python
def test_streaming_foreach_batch_external_column(self):
    table_name = "testTable_foreach_batch_external_column"
    try:
        # Test logic here
        pass
    finally:
        # Clean up the table to avoid affecting other tests
        self.spark.sql(f"DROP TABLE IF EXISTS {table_name}")
```

This approach prevents issues where tests affect catalog-related tests or cause hanging/flaky behavior when run in parallel environments.