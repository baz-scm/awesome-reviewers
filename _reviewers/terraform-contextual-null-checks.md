---
title: Contextual null checks
description: Use type-appropriate null checking strategies based on the context of
  your data. For primitive values, ensure they exist before accessing properties.
  For complex nested structures, use more comprehensive checks like `IsWhollyKnown()`
  instead of simple `IsKnown()` to verify all nested attributes.
repository: hashicorp/terraform
label: Null Handling
language: Go
comments_count: 6
repository_stars: 45532
---

Use type-appropriate null checking strategies based on the context of your data. For primitive values, ensure they exist before accessing properties. For complex nested structures, use more comprehensive checks like `IsWhollyKnown()` instead of simple `IsKnown()` to verify all nested attributes.

When designing interfaces:
- Return `nil` when it leads to clearer calling code (e.g., `if result == nil` vs `if len(result) == 0`)
- Use pointers for optional fields when you need to distinguish between "not set" and "explicitly set to zero value"
- Implement defensive checks before accessing potentially null values

```go
// BAD: May panic if importTarget is not a string type
h.println(fmt.Sprintf("%s: Preparing import... [id=%s]", id.Addr, importTarget.AsString()))

// GOOD: Check type before calling type-specific methods
if importTarget.Type().IsObjectType() {
    h.println(fmt.Sprintf("%s: Preparing import... [identity=%s]", id.Addr, importTarget.GoString()))
} else {
    h.println(fmt.Sprintf("%s: Preparing import... [id=%s]", id.Addr, importTarget.AsString()))
}

// BAD: Using IsKnown() for complex nested structures
if i.Target.IsKnown() {
    // Some attributes might still be unknown
}

// GOOD: Using IsWhollyKnown() for complex nested structures
if i.Target.IsWhollyKnown() {
    // All attributes are guaranteed to be known
}
```

Be consistent in your approach to null handling throughout the codebase, and document expectations about null values in interface definitions.