---
title: optimize algorithmic efficiency
description: Choose efficient data structures and algorithms to minimize computational
  overhead and improve performance. This involves selecting appropriate containers
  based on usage patterns, avoiding unnecessary operations like redundant copies or
  conversions, and leveraging optimized library functions.
repository: electron/electron
label: Algorithms
language: Other
comments_count: 10
repository_stars: 117644
---

Choose efficient data structures and algorithms to minimize computational overhead and improve performance. This involves selecting appropriate containers based on usage patterns, avoiding unnecessary operations like redundant copies or conversions, and leveraging optimized library functions.

Key practices:
- Use performance-optimized containers like `absl::flat_hash_map` instead of `std::unordered_map`, or `base::MakeFixedFlatSet` for compile-time known sets
- Avoid redundant type conversions or parsing by consolidating logic in a single location
- Eliminate unnecessary copies in loops by using references (`const auto& item`) or range-based algorithms
- Prefer standard library algorithms like `base::ranges::any_of` over custom implementations
- Use direct object comparisons instead of converting to intermediate representations when possible
- Avoid unnecessary `std::move` on temporary values that already have move semantics

Example of optimization:
```cpp
// Less efficient - custom loop with copies
for (size_t i = 0; i < val.planes.size(); ++i) {
  auto plane = val.planes[i];  // Unnecessary copy
  // process plane...
}

// More efficient - range-based with references
for (const auto& plane : val.planes) {
  // process plane...
}

// Even better - use library algorithms when applicable
auto v8_planes = base::ToVector(val.planes, [isolate](const auto& plane) {
  // transform logic...
});
```

This approach reduces computational complexity, memory usage, and improves overall performance by making algorithmic choices that align with actual usage patterns.