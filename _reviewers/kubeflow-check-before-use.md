---
title: Check before use
description: Always validate that objects, maps, and other reference types are non-nil
  before attempting to use them. Use early nil checks with clear returns to improve
  code readability and prevent null pointer exceptions.
repository: kubeflow/kubeflow
label: Null Handling
language: Go
comments_count: 3
repository_stars: 15064
---

Always validate that objects, maps, and other reference types are non-nil before attempting to use them. Use early nil checks with clear returns to improve code readability and prevent null pointer exceptions.

For objects:
```go
// Good: Early nil check with informative logging
if pod == nil {
    log.Info("No pod found. Won't update notebook conditions and containerState")
    return status, nil
}
// Now safely use pod...
```

For maps and collections:
```go
// Good: Initialize map if nil before adding items
if currSA.Annotations == nil {
    currSA.Annotations = map[string]string{}
}
currSA.Annotations[key] = value
```

This pattern reduces nesting levels, makes error conditions explicit, and prevents the most common source of runtime panics in Go. When functions receive objects from external sources or other functions, always check their validity before proceeding with operations on them.
