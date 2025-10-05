---
title: Benchmark performance changes
description: Always include performance benchmarks when making changes that could
  impact execution speed, CPU usage, or resource consumption. This prevents performance
  regressions and validates optimization claims.
repository: commaai/openpilot
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 58214
---

Always include performance benchmarks when making changes that could impact execution speed, CPU usage, or resource consumption. This prevents performance regressions and validates optimization claims.

For any performance-related pull request, provide before/after measurements using appropriate benchmarking tools. Include specific metrics like execution time, CPU usage, or throughput improvements.

Example benchmark format:
```python
# Before optimization
old_parse_structs(): 7.900648624985479 seconds
# After optimization  
new_parse_structs(): 5.590290749911219 seconds
```

This practice is essential because performance regressions can be subtle but significant - like the locationd process that "uses 2-3x more CPU than the previous" version, or CAN parsing changes that initially appeared "twice as slow." Without benchmarks, these issues may go unnoticed until they impact system performance in production.

Benchmarks should be run on representative hardware and workloads, and results should demonstrate meaningful improvements or at minimum show no regression in critical performance metrics.