---
title: Avoid unnecessary work
description: Optimize performance by avoiding unnecessary computations, allocations,
  and operations. Use feature gates, lazy evaluation, and conditional logic to prevent
  work that won't be used.
repository: kubernetes/kubernetes
label: Performance Optimization
language: Go
comments_count: 7
repository_stars: 116489
---

Optimize performance by avoiding unnecessary computations, allocations, and operations. Use feature gates, lazy evaluation, and conditional logic to prevent work that won't be used.

Key strategies:
1. **Feature-gated allocations**: Only allocate memory when features are enabled
2. **Lazy computation**: Defer expensive operations until actually needed and cache results
3. **Conditional processing**: Skip loops and operations when conditions aren't met
4. **Efficient data structures**: Choose appropriate algorithms based on expected data size

Example of feature-gated allocation:
```go
// Avoid allocating when feature is disabled
var shareIDs []structured.SharedDeviceID
var deviceCapacities []structured.DeviceConsumedCapacity
if a.enabledConsumableCapacity {
    shareIDs = make([]structured.SharedDeviceID, 0, 20)
    deviceCapacities = make([]structured.DeviceConsumedCapacity, 0, 20)
}
```

Example of conditional processing:
```go
// Performance optimization: skip the for loop if the feature is off
if a.features.DeviceBinding {
    // Only do expensive work when needed
    for _, device := range devices {
        // ... expensive operations
    }
}
```

This approach is particularly important in hot paths, validation code that runs frequently, and resource allocation scenarios where unnecessary work can accumulate significant overhead.