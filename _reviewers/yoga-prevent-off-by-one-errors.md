---
title: prevent off-by-one errors
description: When implementing algorithms that involve spacing, gaps, or iterative
  calculations, carefully verify loop bounds and edge cases to prevent off-by-one
  errors. These errors commonly occur when calculating spacing between N items (which
  requires N-1 gaps, not N gaps) or when applying operations to boundary elements.
repository: facebook/yoga
label: Algorithms
language: C++
comments_count: 2
repository_stars: 18255
---

When implementing algorithms that involve spacing, gaps, or iterative calculations, carefully verify loop bounds and edge cases to prevent off-by-one errors. These errors commonly occur when calculating spacing between N items (which requires N-1 gaps, not N gaps) or when applying operations to boundary elements.

Key areas to scrutinize:
- Gap calculations: For N items, there are N-1 gaps between them
- Boundary conditions: Verify first/last element handling
- Division operations: Check for zero denominators and edge cases
- Loop iterations: Ensure correct start/end conditions

Example from gap calculation:
```cpp
// Wrong: adds gap for all children (N gaps for N items)
for (int i = 0; i < childCount; i++) {
    mainDim += childSize + betweenMainDim;
}

// Correct: adds gap only between children (N-1 gaps for N items)  
const bool isLastChild = i == childCount - 1;
if (isLastChild) {
    betweenMainDim -= gap; // Remove gap for last item
}
```

Always validate your algorithm with boundary cases: single item, empty collection, and maximum expected size. Consider whether conditional checks like `if (lineCount > 1)` are truly necessary or artifacts of avoiding edge case bugs.