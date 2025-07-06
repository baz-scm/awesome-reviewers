---
title: Defer expensive operations
description: Avoid triggering expensive computations prematurely in your code. Operations
  like `collect()`, intensive IO operations, or algorithms with quadratic complexity
  should be deferred until absolutely necessary to prevent wasted computational resources.
repository: pola-rs/polars
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 34296
---

Avoid triggering expensive computations prematurely in your code. Operations like `collect()`, intensive IO operations, or algorithms with quadratic complexity should be deferred until absolutely necessary to prevent wasted computational resources.

For example, instead of:
```python
# This could trigger heavy computation that gets discarded
if strict:
    nrows = first.select(F.len()).collect()[0, 0]
```

Consider deferring the operation:
```python
# Defer the expensive operation to when it's actually needed
pl.scan_iceberg(iceberg_path, snapshot_id=1234567890).collect()
```

When optimizing performance-critical code:
1. Identify operations that could be computationally expensive (IO, collect, complex transformations)
2. Move these operations as late as possible in the execution flow
3. Use benchmarks to verify performance improvements and prevent regressions
4. Be especially vigilant with operations that might have quadratic complexity when scaling

This approach minimizes resource utilization and significantly improves performance, especially when working with large datasets and complex query plans.