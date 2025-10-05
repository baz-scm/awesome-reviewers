---
title: Analyze performance trade-offs
description: Before implementing convenience features or making architectural decisions,
  carefully evaluate their performance implications and hidden costs. Consider factors
  like method call overhead, automatic behavior frequency, and resource utilization
  patterns.
repository: facebook/yoga
label: Performance Optimization
language: Objective-C
comments_count: 3
repository_stars: 18255
---

Before implementing convenience features or making architectural decisions, carefully evaluate their performance implications and hidden costs. Consider factors like method call overhead, automatic behavior frequency, and resource utilization patterns.

Key considerations:
- Choose ivars over properties when readwrite access isn't needed to reduce msgSends
- Avoid redundant code that duplicates existing optimizations (like manual memory management in ARC-enabled code)  
- Be cautious of automatic features that may trigger expensive operations frequently

Example from layout systems:
```objc
// Instead of automatic dirty detection on every layout:
// YGSize newSize = YGMeasureView(node, 0, YGMeasureModeUndefined, 0, YGMeasureModeUndefined);
// Consider the cost: "every leaf node is going to be measured during every single layout call"

// Prefer explicit control when performance matters:
@interface YGLayout ()
@property (nonatomic, assign, readonly) YGNodeRef node; // ivar reduces msgSends
@end
```

Always benchmark assumptions and consider the cumulative impact of seemingly small optimizations, especially in performance-critical paths like layout and rendering.