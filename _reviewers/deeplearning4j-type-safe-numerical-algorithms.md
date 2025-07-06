---
title: Type-safe numerical algorithms
description: 'When implementing numerical algorithms, always use appropriate data
  types to prevent overflow and preserve precision:


  1. Use `Nd4jLong` or `auto` instead of `int` for array indices, dimensions, and
  strides, especially when working with potentially large data structures:'
repository: deeplearning4j/deeplearning4j
label: Algorithms
language: C++
comments_count: 2
repository_stars: 14036
---

When implementing numerical algorithms, always use appropriate data types to prevent overflow and preserve precision:

1. Use `Nd4jLong` or `auto` instead of `int` for array indices, dimensions, and strides, especially when working with potentially large data structures:

```cpp
// Poor implementation - may cause overflow
const int iStride2 = iH * iW;
const int oStride2 = oH * oW;

// Better implementation
const Nd4jLong iStride2 = iH * iW;
const Nd4jLong oStride2 = oH * oW;
```

2. Implement direct type conversions between data types rather than casting through intermediate types (especially floating point) to maintain precision:

```cpp
// Problematic - may lose precision due to floating point limitations
z[i] = static_cast<T>(static_cast<float>(x[i]));

// Better - direct conversion preserves precision
z[i] = static_cast<T>(x[i]);
```

This is particularly important when converting between integer types of different sizes, as floating-point conversions can cause inaccuracies for large values. For specialized numeric types, implement proper conversion operators between them to ensure consistent and precise data handling.