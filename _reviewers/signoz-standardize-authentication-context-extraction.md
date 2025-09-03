---
title: standardize authentication context extraction
description: Always use the standardized `authtypes.ClaimsFromContext` method for
  extracting authentication claims from request context, and handle errors properly.
  This ensures consistent authentication handling across the codebase and prevents
  potential security vulnerabilities from incorrect claim extraction.
repository: SigNoz/signoz
label: Security
language: Go
comments_count: 3
repository_stars: 23369
---

Always use the standardized `authtypes.ClaimsFromContext` method for extracting authentication claims from request context, and handle errors properly. This ensures consistent authentication handling across the codebase and prevents potential security vulnerabilities from incorrect claim extraction.

The correct pattern is:
```go
claims, err := authtypes.ClaimsFromContext(r.Context())
if err != nil {
    render.Error(rw, err)
    return
}
```

Avoid custom claim extraction methods or incorrect error handling patterns like `claims, ok := authtypes.ClaimsFromContext(r.Context())` followed by `if ok != nil` - this can lead to authentication bypasses if the error handling logic is inverted. Using the standardized method ensures proper error propagation and consistent security behavior across all handlers.