---
title: Numerical precision considerations
description: When implementing algorithms involving floating-point calculations, choose
  epsilon values based on the specific domain requirements rather than defaulting
  to system-defined constants. Standard values like `std::numeric_limits<double>::epsilon()`
  are often too small for practical geometric or graphical applications.
repository: maplibre/maplibre-native
label: Algorithms
language: C++
comments_count: 2
repository_stars: 1411
---

When implementing algorithms involving floating-point calculations, choose epsilon values based on the specific domain requirements rather than defaulting to system-defined constants. Standard values like `std::numeric_limits<double>::epsilon()` are often too small for practical geometric or graphical applications.

Instead:
1. Select appropriate epsilon values that account for the scale and precision needs of your specific algorithm
2. Document any precision limitations in code comments
3. Consider defining common epsilon values as named constants for consistency across the codebase

```cpp
// Bad: Using system epsilon which may be too small
if (std::abs(a - b) < std::numeric_limits<double>::epsilon()) {
    // ...
}

// Good: Using domain-appropriate epsilon with documentation
const auto epsilon = 1e-10; // Suitable for geometric calculations at this scale
// Document precision limitations: Results may be unreliable beyond zoom level X
if (std::abs(a - b) < epsilon) {
    // ...
}
```

This approach helps prevent subtle bugs that can occur when numerical comparisons fail due to inappropriate precision thresholds, particularly in geometry processing, graphics rendering, and spatial algorithms.