---
title: Measure before optimizing performance
description: 'Before implementing performance optimizations, measure and validate
  the impact through benchmarks. This applies especially to:


  1. Changes affecting common operations (string conversions, collections)'
repository: elastic/elasticsearch
label: Performance Optimization
language: Java
comments_count: 6
repository_stars: 73104
---

Before implementing performance optimizations, measure and validate the impact through benchmarks. This applies especially to:

1. Changes affecting common operations (string conversions, collections)
2. Modifications to critical paths (search, indexing)
3. Updates to shared resources or services

Example benchmark approach:
```java
@Fork(value = 1)
@Warmup(iterations = 5)
@Measurement(iterations = 5)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class PerformanceBenchmark {
    @Param({"10", "100", "1000"})
    private int size;
    
    @Benchmark
    public void benchmarkOperation() {
        // Test both existing and new implementation
        // Compare results across different input sizes
    }
}
```

Key practices:
- Test with varying input sizes to understand scaling characteristics
- Measure both average case and edge cases
- Compare before/after metrics to quantify improvements
- Consider system-wide impact, not just local optimizations

This approach helps prevent premature optimization and ensures changes provide meaningful performance benefits.
