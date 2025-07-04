---
title: Optimize search operations
description: 'Enhance search algorithm performance by prioritizing common cases, using
  appropriate data structures, and avoiding unnecessary operations.


  When implementing binary search:'
repository: netty/netty
label: Algorithms
language: Java
comments_count: 4
repository_stars: 34227
---

Enhance search algorithm performance by prioritizing common cases, using appropriate data structures, and avoiding unnecessary operations.

When implementing binary search:
1. Consider checking common values first (e.g., the max value) before running a full binary search
2. Add clarifying comments for binary search results like `index = ~index; // same as -(index + 1)`
3. Store repeated calculation results as constants when used in loops
4. Ensure container sizes are powers of two when using bit-masking (`& (size - 1)`) for indexing

Example of optimized binary search with fast-path check:
```java
public int findIndex(int[] sortedArray, int value) {
    // Fast path: check if value is at the max position
    if (sortedArray.length > 0 && sortedArray[sortedArray.length - 1] == value) {
        return sortedArray.length - 1;
    }
    
    // Standard binary search
    int index = Arrays.binarySearch(sortedArray, value);
    if (index < 0) {
        index = ~index; // same as -(index + 1), insertion point
    }
    return index;
}
```

When working with collections, prefer iteration methods that don't create unnecessary copies. For example, use `iterator()` instead of methods that create new collections just for iteration.