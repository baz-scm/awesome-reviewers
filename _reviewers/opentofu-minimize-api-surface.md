---
title: Minimize API surface
description: Design APIs with minimal exposed surface by encapsulating implementation
  details within packages. When designing APIs, expose only what's necessary for consumers
  while keeping internal details hidden.
repository: opentofu/opentofu
label: API
language: Go
comments_count: 4
repository_stars: 25901
---

Design APIs with minimal exposed surface by encapsulating implementation details within packages. When designing APIs, expose only what's necessary for consumers while keeping internal details hidden.

For example, instead of exposing complex types that clients must construct:

```go
// Avoid exporting internal types
type DeprecatedOutputDiagnosticExtra struct {
    Cause DeprecationCause
    wrapped interface{}
}

// Instead, provide wrapper functions that hide implementation details
func DeprecatedOutputDiagnosticOverride(cause DeprecationCause) func() tfdiags.DiagnosticExtraWrapper {
    return func() tfdiags.DiagnosticExtraWrapper {
        return &DeprecatedOutputDiagnosticExtra{
            Cause: cause,
        }
    }
}
```

When making changes to existing APIs:
1. Consider backward compatibility implications, especially with serialized data structures
2. Be cautious with JSON field tags - changing naming conventions can break compatibility
3. Design consistent parameter patterns for CLI interfaces
4. Handle edge cases in API responses, particularly with pagination and nil values

This approach prevents external code from depending on implementation specifics, makes the codebase more maintainable, and enables future refactoring without breaking compatibility.