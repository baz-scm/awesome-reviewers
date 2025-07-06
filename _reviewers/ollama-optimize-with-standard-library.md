---
title: Optimize with standard library
description: When implementing algorithms, prefer using Go's standard library over
  custom implementations or external dependencies for common operations. The standard
  library offers well-tested, efficient implementations for many algorithmic needs.
repository: ollama/ollama
label: Algorithms
language: Go
comments_count: 6
repository_stars: 145704
---

When implementing algorithms, prefer using Go's standard library over custom implementations or external dependencies for common operations. The standard library offers well-tested, efficient implementations for many algorithmic needs.

**Why this matters:**
1. Reduces code complexity and maintenance burden
2. Leverages battle-tested implementations
3. Eliminates external dependencies when possible
4. Often provides better performance

**Examples:**

Instead of implementing custom sorting or search functions:
```go
// Don't reinvent binary search
for low, high := 0, len(arr); low < high; {
    mid := (low + high) / 2
    if arr[mid] < target {
        low = mid + 1
    } else {
        high = mid
    }
}

// Better: Use standard library
idx := slices.BinarySearchFunc(arr, target, func(a, b YourType) int {
    return cmp.Compare(a, b)
})
```

Instead of custom data structures like priority queues:
```go
// Don't use external dependencies for basic data structures
import pq "github.com/emirpasic/gods/queues/priorityqueue"
queue := pq.New()  // External dependency

// Better: Use container/heap from standard library
type tokenHeap []token
// Implement heap.Interface methods: Len, Less, Swap, Push, Pop
// Then use with standard heap package:
h := &tokenHeap{}
heap.Init(h)
heap.Push(h, item)
```

For string operations:
```go
// Avoid manual string manipulation when possible
if strings.HasPrefix(s, prefix) {
    s = strings.TrimSpace(s[len(prefix):])
}

// Better: Use strings.Cut
if after, found := strings.CutPrefix(s, prefix); found {
    s = strings.TrimSpace(after)
}
```

For numeric operations:
```go
// Avoid manual min/max checks
if temperature < 1e-7 {
    temperature = 1e-7
}

// Better: Use built-in min/max functions
temperature = max(temperature, 1e-7)
```