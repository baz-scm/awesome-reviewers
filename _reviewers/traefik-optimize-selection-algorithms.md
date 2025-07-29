---
title: optimize selection algorithms
description: When implementing selection algorithms that choose from a pool of candidates,
  design the algorithm to filter invalid options during the selection process rather
  than using retry logic after selection. Additionally, always include termination
  conditions to prevent infinite loops when no valid candidates remain.
repository: traefik/traefik
label: Algorithms
language: Go
comments_count: 2
repository_stars: 55772
---

When implementing selection algorithms that choose from a pool of candidates, design the algorithm to filter invalid options during the selection process rather than using retry logic after selection. Additionally, always include termination conditions to prevent infinite loops when no valid candidates remain.

The retry approach is inefficient because it may require multiple selection attempts, and each rejected selection wastes computational resources. A filtering approach evaluates constraints once during traversal.

Example of improved selection algorithm:

```go
for {
    // Pick handler with closest deadline
    handler = heap.Pop(b).(*namedHandler)
    
    b.curDeadline = handler.deadline
    handler.deadline += 1 / handler.weight
    heap.Push(b, handler)
    
    // Filter during selection instead of retrying
    if _, down := b.status[handler.name]; !down {
        continue
    }
    
    if _, isFenced := b.fenced[handler.name]; isFenced {
        continue
    }
    
    if handler.passiveHealthChecker != nil && !handler.passiveHealthChecker.AllowRequest() {
        continue
    }
    
    // Always include termination condition
    if allHandlersFenced() {
        return nil, errors.New("no available handlers")
    }
    
    return handler, nil
}
```

This approach eliminates the need for separate retry methods like `nextServerExcluding` and prevents infinite loops when all candidates are invalid.