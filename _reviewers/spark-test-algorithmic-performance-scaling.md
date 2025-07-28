---
title: Test algorithmic performance scaling
description: When implementing or modifying algorithms, especially data structures
  like hash tables, bloom filters, or pattern matching logic, ensure performance characteristics
  are validated across different input scales. Many algorithms exhibit degraded performance
  or correctness issues that only become apparent with large datasets.
repository: apache/spark
label: Algorithms
language: Java
comments_count: 2
repository_stars: 41554
---

When implementing or modifying algorithms, especially data structures like hash tables, bloom filters, or pattern matching logic, ensure performance characteristics are validated across different input scales. Many algorithms exhibit degraded performance or correctness issues that only become apparent with large datasets.

For algorithms that may degrade at scale, create targeted performance tests that cover:
- Small inputs (typical use cases)  
- Medium inputs (stress testing)
- Large inputs (boundary conditions)

When performance testing is impractical for regular CI due to runtime constraints, consider:
- Creating separate benchmark suites that can be run periodically
- Testing at smaller scales that still demonstrate the algorithmic behavior
- Using library methods and established algorithms instead of custom implementations for edge cases

Example from bloom filter testing:
```java
// Test false positive rates at different scales
@Test
public void testBloomFilterScaling() {
    // Test at 1M elements - baseline performance
    testFalsePositiveRate(1_000_000, 0.03, 0.05); // within 5% tolerance
    
    // Test at 100M elements - where degradation may start
    testFalsePositiveRate(100_000_000, 0.03, 0.10); // allow higher tolerance
}
```

Avoid hardcoded checks for algorithmic edge cases. Instead of manual pattern matching like `pattern.equals(lowercaseRegexPrefix)`, use library methods that can properly determine functional equivalence or emptiness.