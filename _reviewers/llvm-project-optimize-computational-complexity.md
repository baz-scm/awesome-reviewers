---
title: optimize computational complexity
description: When implementing algorithms, be mindful of computational complexity
  and optimize for efficiency by avoiding expensive operations and reusing existing
  computations where possible.
repository: llvm/llvm-project
label: Algorithms
language: C++
comments_count: 4
repository_stars: 33702
---

When implementing algorithms, be mindful of computational complexity and optimize for efficiency by avoiding expensive operations and reusing existing computations where possible.

Key principles:

1. **Avoid expensive object operations**: When sorting or manipulating heavy objects, work with pointers or lightweight references instead of the objects themselves. For example, when sorting a collection of large structures, sort an array of pointers rather than moving the actual objects.

2. **Reuse existing computations**: Before performing expensive calculations, check if equivalent results already exist that can be reused with minimal adjustment. Look for opportunities to reuse intermediate results rather than recomputing from scratch.

3. **Ensure deterministic ordering**: Use consistent ordering (e.g., sorting) for data structures to avoid non-deterministic behavior that can lead to inconsistent optimization results or algorithmic outcomes.

4. **Consider phase ordering**: Be aware that the sequence of applying algorithmic phases can significantly impact the final result quality. Design algorithms with careful consideration of when each optimization or transformation should be applied.

Example from the codebase:
```cpp
// Instead of sorting heavy objects directly:
// std::sort(heavyObjects.begin(), heavyObjects.end());

// Sort pointers to avoid expensive object movement:
SmallVector<LSRUse *, 16> sortedPointers;
for (auto &use : heavyObjects)
  sortedPointers.push_back(&use);
std::sort(sortedPointers.begin(), sortedPointers.end(), comparator);

// Reuse existing computations when possible:
if (existingResult && canReuseWithOffset(existingResult, offset)) {
  return adjustWithOffset(existingResult, offset);
}
```

This approach reduces computational overhead while maintaining algorithmic correctness and improving overall performance.