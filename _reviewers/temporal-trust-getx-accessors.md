---
title: Trust GetX accessors
description: When working with protocol buffer messages or similar objects that provide
  GetX() accessor methods, avoid redundant nil checks before calling these methods.
  GetX() methods are designed to handle nil receivers safely, allowing for cleaner
  and more concise code.
repository: temporalio/temporal
label: Null Handling
language: Go
comments_count: 4
repository_stars: 14953
---

When working with protocol buffer messages or similar objects that provide GetX() accessor methods, avoid redundant nil checks before calling these methods. GetX() methods are designed to handle nil receivers safely, allowing for cleaner and more concise code.

**Good practice:**
```go
// These GetX() methods handle nil receivers safely
userData.GetData().GetPerType()[int32(taskQueueType)]
for _, v := range typedUserData.GetDeploymentData().GetVersions() {
    // Process versions safely even if typedUserData is nil
}
```

**Avoid unnecessary checks:**
```go
// Redundant and verbose - these checks are unnecessary
if userData != nil {
    if userData.GetData() != nil {
        typedUserData := userData.GetData().GetPerType()[int32(pm.Partition().TaskType())]
        // ...
    }
}
```

**Important caveats:**
1. This only applies to methods specifically designed to handle nil (typically GetX methods)
2. Direct field access or map lookups still require nil checks
3. When assigning to fields or variables, checks may be needed to avoid null reference errors

Remember that while method chaining with GetX() is safe for retrieval operations, operations that modify values may still require explicit nil checks.