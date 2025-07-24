---
title: Safe collection modification
description: When modifying collections during iteration, use safe patterns to avoid
  subtle bugs and undefined behavior. Common unsafe patterns include modifying map
  values during range iteration, capturing loop variables by reference, and deleting
  from slices while iterating.
repository: docker/compose
label: Algorithms
language: Go
comments_count: 3
repository_stars: 35858
---

When modifying collections during iteration, use safe patterns to avoid subtle bugs and undefined behavior. Common unsafe patterns include modifying map values during range iteration, capturing loop variables by reference, and deleting from slices while iterating.

**Safe Patterns:**

1. **Map modification**: Create new collections or update after iteration
```go
// Instead of modifying during iteration:
for name, service := range set {
    service.Scale++  // Unsafe if service is a value
    set[name] = service  // Update map after modification
}
```

2. **Variable capture**: Avoid pointer capture of loop variables
```go
// Safe pattern - explicit assignment:
for k, v := range source {
    v := v  // Create new variable to avoid pointer capture
    dest[k] = &v
}
```

3. **Slice modification**: Use new slice or reverse iteration
```go
// Instead of deleting during forward iteration:
// Create new slice and copy elements to keep
newVolumes := make([]Volume, 0, len(s.Volumes))
for _, vol := range s.Volumes {
    if shouldKeep(vol) {
        newVolumes = append(newVolumes, vol)
    }
}
s.Volumes = newVolumes
```

These patterns prevent common algorithmic errors where collection state changes during iteration lead to skipped elements, incorrect references, or unpredictable behavior.