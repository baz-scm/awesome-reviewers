---
title: ensure comprehensive test coverage
description: Tests should validate all relevant code paths and actually exercise the
  functionality they claim to test. When adding tests for new features, ensure they
  stress the new behavior rather than just existing functionality that was already
  covered.
repository: duckdb/duckdb
label: Testing
language: Python
comments_count: 2
repository_stars: 32061
---

Tests should validate all relevant code paths and actually exercise the functionality they claim to test. When adding tests for new features, ensure they stress the new behavior rather than just existing functionality that was already covered.

For functions with multiple execution paths (like optional parameters), write test cases that cover each path:

```python
def test_try_to_timestamp(self, spark):
    df = spark.createDataFrame([('1997-02-28 10:30:00',), ('2024-01-01',), ('invalid')], ['t'])
    # Test default format (format=None)
    res = df.select(F.try_to_timestamp(df.t).alias('dt')).collect()
    # Test explicit format
    res_fmt = df.select(F.try_to_timestamp(df.t, 'yyyy-MM-dd HH:mm:ss').alias('dt')).collect()
```

When testing new functionality, use inputs that specifically exercise the new behavior rather than inputs that would work with the old implementation. Avoid test cases where "your string is just 'i' this was already covered by the old behavior" - instead, create test cases that would fail without the new functionality.