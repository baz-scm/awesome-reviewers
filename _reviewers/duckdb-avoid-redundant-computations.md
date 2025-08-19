---
title: avoid redundant computations
description: Move loop-invariant conditions and computations outside of iteration
  blocks to improve performance and reduce redundant processing. When the same check
  or calculation doesn't depend on loop variables, extract it to run once before the
  loop rather than repeating it for each iteration.
repository: duckdb/duckdb
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 32061
---

Move loop-invariant conditions and computations outside of iteration blocks to improve performance and reduce redundant processing. When the same check or calculation doesn't depend on loop variables, extract it to run once before the loop rather than repeating it for each iteration.

For example, instead of checking the same condition inside every loop iteration:

```python
for regression in regression_list:
    if isinstance(time_old, float) and isinstance(time_new, float):
        # process regression
```

Extract the invariant check outside the loop:

```python
if isinstance(time_old, float) and isinstance(time_new, float):
    geomean_time_slower = time_new <= time_old
    for regression in regression_list:
        if geomean_time_slower and individual_regression_diff_perc <= 10.0:
            # process regression
```

This optimization is particularly important in performance-critical code paths, benchmarking systems, and data processing pipelines where loops may process large datasets. Additionally, avoid duplicate processing by leveraging existing classifications or computations rather than recalculating the same values.