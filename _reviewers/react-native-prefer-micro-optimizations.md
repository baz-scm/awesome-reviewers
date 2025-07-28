---
title: Prefer micro-optimizations
description: Apply small performance improvements that accumulate to significant gains.
  Focus on efficient memory usage, API choices, and avoiding unnecessary operations.
repository: facebook/react-native
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 123178
---

Apply small performance improvements that accumulate to significant gains. Focus on efficient memory usage, API choices, and avoiding unnecessary operations.

Key practices:
- Use references instead of copies when possible: `auto& dynamic = std::get<folly::dynamic>(value_)` instead of `folly::dynamic dynamic = std::get<folly::dynamic>(value_)`
- Prefer faster API variants: use `getObject()` instead of `asObject()` when you've already validated with `isObject()` - it's faster because it uses an assert
- Use move semantics and emplace for containers: `result.emplace(propertyNameString, std::move(property))` instead of `result[propertyNameString] = property` for better performance with no unnecessary copies
- Avoid expensive memory operations: use stack allocation `CGFloat locations[colorStops.size()]` instead of `malloc(sizeof(CGFloat) * colorStops.size())`

These micro-optimizations are especially important in performance-critical code paths where small improvements compound across many operations.