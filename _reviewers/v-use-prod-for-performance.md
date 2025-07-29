---
title: use `-prod` for performance
description: Always use the `-prod` compiler flag when building performance-critical
  code or running benchmarks. The `-prod` flag automatically enables essential optimization
  settings including `-O3` and `-flto` (Link Time Optimization), eliminating the need
  to manually specify these common performance flags.
repository: vlang/v
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 36582
---

Always use the `-prod` compiler flag when building performance-critical code or running benchmarks. The `-prod` flag automatically enables essential optimization settings including `-O3` and `-flto` (Link Time Optimization), eliminating the need to manually specify these common performance flags.

This approach ensures consistent optimization across different build scenarios and reduces the likelihood of forgetting important performance flags. For additional architecture-specific optimizations, you can combine `-prod` with targeted flags:

```bash
# For performance-critical applications
v -cc gcc -prod -cflags "-std=c17 -march=native -mtune=native" .

# For benchmarking
v -prod run bench/bench.v
```

Using `-prod` as the foundation provides a reliable baseline for performance optimization while allowing for additional customization when needed.