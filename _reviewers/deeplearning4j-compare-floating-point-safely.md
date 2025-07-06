---
title: Compare floating-point safely
description: 'When implementing numerical algorithms, never compare floating-point
  values directly for equality due to precision errors. Instead:


  1. Use an epsilon threshold for comparisons:'
repository: deeplearning4j/deeplearning4j
label: Algorithms
language: Java
comments_count: 4
repository_stars: 14036
---

When implementing numerical algorithms, never compare floating-point values directly for equality due to precision errors. Instead:

1. Use an epsilon threshold for comparisons:
```java
private static final double EPSILON = 1e-6;  // Choose appropriate precision

// Instead of this:
if (backpropGradient == 0.0) { ... }

// Do this:
if (Math.abs(backpropGradient) < EPSILON) { ... }
```

2. For equality comparisons in algorithms like sorting or searching, use built-in methods:
```java
// Instead of manually comparing with multiple conditions:
if (lhs.fitness < rhs.fitness)
    return 1;
else if (rhs.fitness < lhs.fitness)
    return -1;
return 0;

// Use the built-in compare method:
return Double.compare(rhs.getFitness(), lhs.getFitness());
```

3. Choose appropriate epsilon values based on your application domain:
   - For double precision: typically 1e-6 to 1e-12
   - For machine learning: often 1e-5 to 1e-7
   - For financial calculations: may require stricter precision

4. In tests, be explicit about data types when comparing arrays to avoid hidden type conversion issues.

Following these practices prevents subtle bugs in sorting, searching, and numerical algorithms where small differences in representation can lead to incorrect results.