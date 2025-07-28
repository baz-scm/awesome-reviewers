---
title: cost-based algorithmic decisions
description: When implementing algorithmic transformations and optimizations, use
  cost analysis and profitability heuristics to guide decision-making rather than
  applying transformations blindly. This includes choosing appropriate data structures
  based on access patterns, placing optimizations at the correct architectural level,
  and validating that algorithmic changes...
repository: llvm/llvm-project
label: Algorithms
language: Other
comments_count: 5
repository_stars: 33702
---

When implementing algorithmic transformations and optimizations, use cost analysis and profitability heuristics to guide decision-making rather than applying transformations blindly. This includes choosing appropriate data structures based on access patterns, placing optimizations at the correct architectural level, and validating that algorithmic changes actually improve performance.

Key principles:
1. **Data structure selection**: Choose between alternatives based on access patterns. For example, use a map when you need efficient lookups and only want the most recent entry, but use a vector when linear iteration is acceptable and the number of elements is small.

2. **Optimization placement**: Place algorithmic optimizations where they can be most effective. Constant folding should be in generic optimization passes rather than specialized locations, and profitability checks should override general heuristics when needed.

3. **Performance validation**: Always measure the impact of algorithmic changes. Cost models can be wrong, leading to performance regressions that need to be detected and addressed.

Example from loop transformations:
```cpp
// Use profitability analysis to guide loop interchange
bool shouldInterchange = profitabilityCheck(outerLoop, innerLoop);
if (shouldInterchange && canVectorizeInnerLoop(outerLoop)) {
  // Move vectorizable loop to innermost position
  interchangeLoops(outerLoop, innerLoop);
}
```

The goal is to make algorithmic decisions based on measurable criteria rather than assumptions, ensuring that optimizations actually improve performance for the target use cases.