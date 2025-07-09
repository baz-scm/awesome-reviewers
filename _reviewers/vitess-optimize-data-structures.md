---
title: Optimize data structures
description: 'Choose and implement data structures with careful consideration of algorithmic
  complexity, memory usage, and Go''s specific performance characteristics. Pay attention
  to:'
repository: vitessio/vitess
label: Algorithms
language: Go
comments_count: 6
repository_stars: 19815
---

Choose and implement data structures with careful consideration of algorithmic complexity, memory usage, and Go's specific performance characteristics. Pay attention to:

1. **Placement of operations in code flow**: Consider when and where operations are performed, especially in loops or before early returns.

```go
// Be careful with operations inside loops
func (set Mysql56GTIDSet) AddGTIDInPlace(gtid GTID) GTIDSet {
    // ...
    for _, iv := range intervals {
        // ... processing logic ...
        
        // Incorrect: Updating data structure in every loop iteration
        set[gtid56.Server] = newIntervals
    }
    // Correct: Update once after loop completes (when appropriate)
    set[gtid56.Server] = newIntervals
}
```

However, be mindful of early returns that might skip operations:

```go
// Early returns may require updates within the loop
for _, iv := range intervals {
    if condition {
        // Update needed here if we might return
        set[gtid56.Server] = newIntervals
        return set
    }
}
```

2. **Efficient implementation choices**: Choose implementations that avoid unnecessary overhead:
   - Prefer direct binary operations over reflection-based alternatives like `binary.Write`
   - Consider specialized data structures for specific use cases (e.g., Disjoint Set Union for transitive closures)
   - Order type assertions from most specific to most general to avoid unnecessary checks

3. **Accurate metrics and counts**: Ensure methods that report on data structure state (like length or size) accurately reflect the true state:
   - Avoid double-counting elements in queue implementations
   - Be precise about what your metrics represent (buffer capacity vs. element count)

By thoughtfully designing and implementing your data structures, you can significantly improve both performance and maintainability of your code.