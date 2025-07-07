---
title: Choose efficient implementations
description: When implementing algorithms, prioritize both correctness and performance
  by selecting appropriate data structures, optimizing memory usage, and leveraging
  language features.
repository: tensorflow/tensorflow
label: Algorithms
language: Other
comments_count: 6
repository_stars: 190625
---

When implementing algorithms, prioritize both correctness and performance by selecting appropriate data structures, optimizing memory usage, and leveraging language features.

### Comparison functions
Implement proper three-way comparisons that handle equality cases correctly:

```cpp
// INCORRECT: Returns only -1 or 1, missing 0 for equality
inline int WeightedDeltaCompare(const void* const a, const void* const b) {
  return (reinterpret_cast<const WeightedDelta*>(a)->delta -
          reinterpret_cast<const WeightedDelta*>(b)->delta) <= 0 ? 1 : -1;
}

// CORRECT: Returns -1, 0, or 1 for proper ordering
inline int WeightedDeltaCompare(const void* const a, const void* const b) {
    float delta_a = reinterpret_cast<const WeightedDelta*>(a)->delta;
    float delta_b = reinterpret_cast<const WeightedDelta*>(b)->delta;
    if (delta_a < delta_b) return -1;
    if (delta_a > delta_b) return 1;
    return 0;
}
```

### Memory optimization
Defer memory allocation until needed to avoid unnecessary resource consumption:

```cpp
// INEFFICIENT: Creates vector regardless of whether it will be used
std::vector<std::uint16_t> uint16_data;
if (GetDataType() != QNN_DATATYPE_SFIXED_POINT_16) {
  return;
}

// EFFICIENT: Only creates vector when it will be used
if (GetDataType() != QNN_DATATYPE_SFIXED_POINT_16) {
  return;
}
std::vector<std::uint16_t> uint16_data;
```

### Vector initialization
Use std::iota for sequential initialization instead of manual loops:

```cpp
// INEFFICIENT: Manual population of sequential values
std::vector<TypeParam> values;
for (int i = 0; i < 32768; i++) {
  values.push_back(i);
}

// EFFICIENT: Use std::iota for sequential initialization
std::vector<TypeParam> values(32768);
std::iota(values.begin(), values.end(), TypeParam(0));
```

### Resource management
Use std::move when transferring collections to optimize performance:

```cpp
// INEFFICIENT: Copying elements one by one
for (const auto& op_wrapper : op_wrappers) {
  graph_op_wrappers.emplace_back(op_wrapper);
}

// EFFICIENT: Moving entire collection at once
std::move(op_wrappers.begin(), op_wrappers.end(),
          std::back_inserter(graph_op_wrappers));
```

### Mathematical correctness
Ensure mathematical algorithms handle edge cases and are implemented according to their proper definitions:

```cpp
// INCORRECT: Wrong implementation of floormod
// floormod(x,y) = (x/y) - floor(x/y)

// CORRECT: Proper implementation with additional multiplication
// floormod(x,y) = ((x/y) - floor(x/y))*y
```

### Numeric stability
Be vigilant about integer overflow, especially in calculations involving ranges or large numbers:

```cpp
// VULNERABLE to overflow when limit-start is large
auto size_auto = Eigen::numext::ceil(Eigen::numext::abs((limit - start) / delta));

// SAFER approach to avoid overflow
auto size_auto = Eigen::numext::ceil(
    Eigen::numext::abs((limit / delta) - (start / delta)));
```