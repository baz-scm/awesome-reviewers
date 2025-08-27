---
title: Avoid redundant operations
description: Eliminate duplicate computations, unnecessary API calls, and redundant
  processing to improve performance and reduce system load. This includes avoiding
  duplicate function calls, minimizing API server requests, and implementing early
  returns or caching to prevent redundant work.
repository: volcano-sh/volcano
label: Performance Optimization
language: Go
comments_count: 7
repository_stars: 4899
---

Eliminate duplicate computations, unnecessary API calls, and redundant processing to improve performance and reduce system load. This includes avoiding duplicate function calls, minimizing API server requests, and implementing early returns or caching to prevent redundant work.

Key strategies:
- **Eliminate duplicate function calls**: Call expensive functions once and reuse results instead of calling multiple times
- **Minimize API server load**: Move expensive operations like API requests inside conditional blocks to avoid unnecessary calls when conditions aren't met
- **Implement caching**: Cache expensive computations and use early returns to avoid redundant processing
- **Avoid redundant processing**: Check if work has already been done before repeating operations

Example from the discussions:
```go
// Bad: Calling calculateWeight twice
hyperNodeTierWeight: calculateWeight(arguments),
taskNumWeight:       calculateWeight(arguments),

// Good: Call once and reuse
weight := calculateWeight(arguments)
hyperNodeTierWeight: weight,
taskNumWeight:       weight,
```

```go
// Bad: Always calculating expensive operation
minMember := pg.getMinMemberFromUpperRes(pod) // Heavy API operation
if err := pg.createNormalPodPGIfNotExist(pod); err != nil {

// Good: Only calculate when needed
if err := pg.createNormalPodPGIfNotExist(pod); err != nil {
    // Only calculate minMember if podgroup creation is needed
    minMember := pg.getMinMemberFromUpperRes(pod)
}
```

This approach reduces computational overhead, decreases API server load, and improves overall system performance, especially in large-scale environments where these optimizations compound significantly.