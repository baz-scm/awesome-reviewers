---
title: optimize algorithmic choices
description: Choose efficient algorithms and data structures to improve performance
  and reduce computational overhead. This involves selecting appropriate containers,
  avoiding unnecessary operations, and leveraging language features for optimization.
repository: microsoft/terminal
label: Algorithms
language: C++
comments_count: 8
repository_stars: 99242
---

Choose efficient algorithms and data structures to improve performance and reduce computational overhead. This involves selecting appropriate containers, avoiding unnecessary operations, and leveraging language features for optimization.

Key optimization strategies:
- **Use specialized containers**: Prefer `til::static_map` over `std::unordered_map` for compile-time initialization, or `wil::to_vector` for collection cloning
- **Leverage return values**: Use the return value of operations like `insert()` instead of separate `contains()` + `insert()` calls
- **Apply move semantics**: Use `std::move` when transferring ownership, especially with expensive objects like `std::filesystem::path`
- **Choose better algorithms**: Replace expensive operations like `lstrcmpiW` with more efficient alternatives like ICU functions for Unicode handling
- **Avoid unnecessary copies**: Be careful with reference binding to prevent breaking return value optimization

Example of inefficient vs optimized approach:
```cpp
// Inefficient: separate contains + insert
if (!state->DismissedBadges->contains(badgeId)) {
    state->DismissedBadges->insert(badgeId);
    inserted = true;
}

// Optimized: use insert return value
auto [iter, inserted] = state->DismissedBadges->insert(badgeId);
```

For mathematical computations, choose appropriate distance metrics - use squared Euclidean distance `r*r + g*g + b*b` instead of Manhattan distance `abs(r) + abs(g) + abs(b)` for color comparisons to better represent perceptual differences.