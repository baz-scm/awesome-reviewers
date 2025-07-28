---
title: avoid unnecessary allocations
description: When implementing algorithms and data structure operations, avoid unnecessary
  memory allocations, object creation, and data copying that can impact performance.
  Look for opportunities to leverage existing objects, references, and lazy evaluation
  patterns.
repository: facebook/react-native
label: Algorithms
language: C++
comments_count: 2
repository_stars: 123178
---

When implementing algorithms and data structure operations, avoid unnecessary memory allocations, object creation, and data copying that can impact performance. Look for opportunities to leverage existing objects, references, and lazy evaluation patterns.

Key optimization strategies:
- Use polymorphism instead of creating new objects when type compatibility exists (Liskov Substitution Principle)
- Prefer const references over copying when data won't be modified
- Implement lazy evaluation with optional types to defer expensive operations until needed

Example of unnecessary allocation:
```cpp
// Avoid: Creating unnecessary shared_ptr when type already matches
dispatchEvent("scrollEndDrag", std::make_shared<ScrollEndDragEvent>(scrollEvent));

// Better: Let polymorphism handle the type conversion
dispatchScrollViewEvent("scrollEndDrag", scrollEvent);
```

Example of unnecessary copying:
```cpp
// Avoid: Always copying the list
auto children = shadowNode.getChildren();

// Better: Use reference when no modification needed
const auto& children = shadowNode.getChildren();

// Or: Use lazy evaluation for conditional modification
std::optional<ListOfShared> modifiedChildren;
// Only copy when first modification is needed
```

This approach reduces computational complexity and memory pressure in performance-critical code paths.