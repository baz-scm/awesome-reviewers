---
title: avoid unnecessary allocations
description: Minimize performance overhead by avoiding unnecessary memory allocations,
  expensive data structures, and redundant object creation. Choose appropriate data
  types and parameter passing methods based on actual requirements rather than convenience.
repository: llvm/llvm-project
label: Performance Optimization
language: C++
comments_count: 7
repository_stars: 33702
---

Minimize performance overhead by avoiding unnecessary memory allocations, expensive data structures, and redundant object creation. Choose appropriate data types and parameter passing methods based on actual requirements rather than convenience.

Key practices:
- Use simpler data types when complex ones aren't needed (e.g., `int32_t[]` instead of `SmallVector<APInt>` for fixed-size arrays)
- Pass parameters efficiently (`StringRef` instead of `const std::string&`, `std::move()` for transferring ownership)
- Avoid expensive utility classes when simpler alternatives exist (e.g., replacing `TrackingVH` with visited sets where possible)
- Reuse resources instead of creating new ones (e.g., reusing thread arrays in loops rather than creating new ones each iteration)
- Use efficient string building methods (`std::stringstream` or `formatv()` instead of repeated concatenation)
- Prevent memory leaks from dynamic allocations by using RAII or smart pointers

Example of inefficient vs efficient approaches:
```cpp
// Inefficient: Creates many temporary strings and copies
std::string result = "{ ";
for (size_t i = 0; i < items.size(); ++i) {
  result += "\"" + items[i].first + "\", " + items[i].second;
  if (i < items.size() - 1) result += ", ";
}

// Efficient: Uses stringstream to avoid copies
std::stringstream ss;
ss << "{ ";
for (size_t i = 0; i < items.size(); ++i) {
  ss << "\"" << items[i].first << "\", " << items[i].second;
  if (i < items.size() - 1) ss << ", ";
}
std::string result = ss.str();
```

Profile performance-critical code paths to identify where expensive operations like `TrackingVH` creation or unnecessary allocations are causing bottlenecks, then replace them with more efficient alternatives.