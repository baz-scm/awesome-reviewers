---
title: Prefer early null returns
description: Use early return patterns with null checks to reduce nesting and improve
  code readability. Avoid unnecessary null checks for values that are guaranteed to
  be non-nil, and prefer length checks over nil checks for slices.
repository: kubernetes/kubernetes
label: Null Handling
language: Go
comments_count: 5
repository_stars: 116489
---

Use early return patterns with null checks to reduce nesting and improve code readability. Avoid unnecessary null checks for values that are guaranteed to be non-nil, and prefer length checks over nil checks for slices.

When checking for null values, use early returns to handle the null case first, then continue with the main logic. This pattern reduces cognitive load and prevents deeply nested conditional blocks.

For optional fields that are feature-gated or alpha, avoid checking default values alongside null checks - the null check alone is sufficient.

Example patterns:
```go
// Good: Early return pattern
if result.ShareID == nil {
    allocatedDevices.Insert(deviceID)
    continue
}
sharedDeviceID := structured.MakeSharedDeviceID(deviceID, *result.ShareID)
allocatedSharedDeviceIDs.Insert(sharedDeviceID)

// Good: Simplified null equality check
if statusA == nil || statusB == nil {
    return statusA == statusB
}

// Good: Length check instead of nil check for slices
if len(bindingConditions) == 0 && len(bindingFailureConditions) > 0 {
    // handle error case
}

// Good: Simple null check for optional fields
if device.ShareID != nil {
    // process ShareID
}

// Avoid: Unnecessary null checks for guaranteed non-nil values
if f.handle != nil && hasExtendedResource { // f.handle is always non-nil
```

This approach makes null handling explicit, reduces the chance of null reference errors, and creates more maintainable code by clearly separating null handling from business logic.