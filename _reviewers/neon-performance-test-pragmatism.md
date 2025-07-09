---
title: Performance test pragmatism
description: 'When designing performance tests, focus on efficiency and meaningful
  insights rather than exhaustive combinations. Consider these principles:


  1. **Limit parameter combinations** to avoid excessive test duration. For example,
  instead of:'
repository: neondatabase/neon
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 19015
---

When designing performance tests, focus on efficiency and meaningful insights rather than exhaustive combinations. Consider these principles:

1. **Limit parameter combinations** to avoid excessive test duration. For example, instead of:
```python
@pytest.mark.parametrize(
    "pipelining_config,ps_io_concurrency,l0_stack_height,queue_depth,name",
    [
        (config, ps_io_concurrency, l0_stack_height, queue_depth, f"{dataclasses.asdict(config)}")
        for config in LATENCY_CONFIGS
        for ps_io_concurrency in PS_IO_CONCURRENCY
        for queue_depth in [1, 2, 3, 4, 16, 32]
        for l0_stack_height in [0, 3, 10]
    ],
)
```
Consider testing only critical parameter combinations such as production values and a few boundary cases.

2. **Use robust performance measurement techniques** when comparing optimizations. For significant features, measure performance both with and without the optimization and average multiple runs to account for system variability:
```python
# Run each test multiple times and average the results
run_times_with_feature = []
run_times_without_feature = []
for _ in range(SAMPLE_SIZE):
    run_times_with_feature.append(measure_execution(feature_enabled=True))
    run_times_without_feature.append(measure_execution(feature_enabled=False))
    
avg_with_feature = sum(run_times_with_feature) / len(run_times_with_feature)
avg_without_feature = sum(run_times_without_feature) / len(run_times_without_feature)
```

3. **Balance thoroughness with execution time**. Consider randomized parameter selection for exploratory testing when exhaustive testing is impractical, but ensure values are logged for reproducibility.