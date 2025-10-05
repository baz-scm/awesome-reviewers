---
title: Measure optimization trade-offs
description: Always measure and document the impact of performance optimizations before
  implementing them. When making optimization decisions, quantify the benefits (size
  reduction, speed improvement) against the costs (build time, code complexity, maintainability).
repository: facebook/yoga
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 18255
---

Always measure and document the impact of performance optimizations before implementing them. When making optimization decisions, quantify the benefits (size reduction, speed improvement) against the costs (build time, code complexity, maintainability).

Key practices:
- Benchmark before and after changes with specific metrics
- Document measured improvements in code reviews
- Consider multiple optimization approaches and compare results
- Balance different types of performance (binary size vs execution speed vs build time)

Example from compiler optimizations:
```makefile
# Measured impact: 10kb size reduction
-fno-exceptions -fno-rtti  # Disables C++ features for size savings
-flto                      # Link-time optimization for performance (2x build time)
```

Example from memory optimization:
```cpp
// Before: 12 bytes overhead per node (4 + 8 bytes)
struct YGNode {
    uint32_t gDepth = 0;        // 4 bytes per node
    YGNodeRef pRoot = nullptr;  // 8 bytes per node
};

// After: Pass values through function parameters instead
void calculateLayout(YGNode* node, uint32_t depth, uint32_t generation);
```

This approach ensures optimizations provide real value and helps teams make informed decisions about performance trade-offs.