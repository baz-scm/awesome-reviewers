---
title: Add explicit nil checks
description: Always add explicit nil checks before accessing object properties and
  after type assertions to prevent null pointer exceptions and runtime panics. Even
  when type assertions succeed, the underlying value can still be nil, requiring additional
  validation.
repository: volcano-sh/volcano
label: Null Handling
language: Go
comments_count: 7
repository_stars: 4899
---

Always add explicit nil checks before accessing object properties and after type assertions to prevent null pointer exceptions and runtime panics. Even when type assertions succeed, the underlying value can still be nil, requiring additional validation.

Key scenarios requiring nil checks:
1. **After type assertions**: Check if the asserted value is nil even when type assertion succeeds
2. **Before property access**: Validate objects are not nil before accessing their fields
3. **Function parameters**: Add nil checks for pointer parameters that could be nil
4. **Map/collection access**: Verify collections exist before operations

Example from the discussions:
```go
// Before: Unsafe type assertion
if devices, ok := node.Others[val].(api.Devices); ok {
    code, msg, err := devices.FilterNode(task.Pod) // Potential panic if devices is nil
}

// After: Safe with nil check
if dev, ok := node.Others[val].(api.Devices); ok {
    if dev == nil {
        continue // or handle appropriately
    }
    code, msg, err := dev.FilterNode(task.Pod)
}

// Before: Unsafe property access
func isNodeUnschedulable(node *v1.Node) bool {
    return node.Spec.Unschedulable // Potential panic if node is nil
}

// After: Safe with nil check
func isNodeUnschedulable(node *v1.Node) bool {
    if node == nil {
        return false
    }
    return node.Spec.Unschedulable
}
```

This practice prevents runtime crashes and makes code more robust, especially when dealing with interface types and optional parameters.