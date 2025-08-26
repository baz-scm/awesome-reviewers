---
title: measure performance implications
description: When making design decisions that could impact performance, evaluate
  resource implications and provide concrete measurements rather than assumptions.
  Consider memory usage, binary size, and allocation patterns in your choices.
repository: tree-sitter/tree-sitter
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 21799
---

When making design decisions that could impact performance, evaluate resource implications and provide concrete measurements rather than assumptions. Consider memory usage, binary size, and allocation patterns in your choices.

For API design, prefer memory-efficient data structures when they provide equivalent functionality. For example, use symbol IDs instead of strings when the IDs serve the same purpose but consume less memory and reduce binary size.

When concerned about performance costs, benchmark the actual impact:

```cpp
// Instead of assuming new/delete is slow, measure it
$ for x in $(echo "1 2 3 4 5"); do time ./out/Test/tests >/dev/null; done
real    0m19.423s  // Before optimization
real    0m20.394s  // After change - minimal impact
```

Always validate performance assumptions with data, especially for frequently called code paths or resource-constrained environments like WebAssembly.