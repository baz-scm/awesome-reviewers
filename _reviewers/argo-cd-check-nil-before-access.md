---
title: Check nil before access
description: Always verify that pointers and nested struct fields are not nil before
  accessing their members to prevent runtime panics. This is especially important
  when dealing with optional configuration fields, middleware components, and API
  responses where certain fields may not be initialized.
repository: argoproj/argo-cd
label: Null Handling
language: Go
comments_count: 5
repository_stars: 20149
---

Always verify that pointers and nested struct fields are not nil before accessing their members to prevent runtime panics. This is especially important when dealing with optional configuration fields, middleware components, and API responses where certain fields may not be initialized.

Before accessing nested fields, check each level for nil:

```go
// Bad - can cause nil pointer panic
*spec.SyncPolicy.Automated.Enable = true

// Good - check each level
if spec.SyncPolicy == nil {
    spec.SyncPolicy = &argoappv1.SyncPolicy{}
}
if spec.SyncPolicy.Automated == nil {
    spec.SyncPolicy.Automated = &argoappv1.SyncPolicyAutomated{}
}
*spec.SyncPolicy.Automated.Enable = true
```

For optional fields that may be missing, return nil gracefully rather than panicking:

```go
// Good - handle missing claims safely
if _, ok := m["iat"]; !ok {
    return nil, nil // Claim is missing
}
```

Consider creating helper methods on structs to encapsulate nil checks, making the code more readable and preventing repeated nil checking logic throughout the codebase.