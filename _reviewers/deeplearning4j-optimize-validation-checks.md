---
title: Optimize validation checks
description: 'When implementing validation and requirement checks, balance thoroughness
  with performance considerations. Critical validations should remain unconditional,
  but optimize their implementation to minimize performance impact:'
repository: deeplearning4j/deeplearning4j
label: Performance Optimization
language: CUDA
comments_count: 2
repository_stars: 14036
---

When implementing validation and requirement checks, balance thoroughness with performance considerations. Critical validations should remain unconditional, but optimize their implementation to minimize performance impact:

1. Use short-circuit evaluation with logical operators (&&) to avoid unnecessary validations
2. Implement lazy evaluation for complex checks using lambdas
3. Consider conditionally enabling detailed error reporting in debug mode only
4. Pay special attention to validation code in performance-sensitive paths

```cpp
// Good practice - using short-circuit and lazy evaluation
Requirements req("CUDNN OPERATION");
req.expectIn(makeInfoVariable(dataType, TYPE_MSG), {ValidTypes}) &&
req.expectTrue([&]() { 
    // Complex validation only evaluated if previous check passes
    return validateComplexCondition(input); 
});

// Avoid unconditional evaluation of everything, especially in hot paths
// auto info = getDetailedInfo(input);  // Always executed regardless of need
// if (!meetsRequirements(info)) return false;
```

This approach ensures your code remains robust with meaningful error reporting while minimizing performance overhead in production environments.