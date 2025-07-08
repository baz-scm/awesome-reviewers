---
title: Choose appropriate API types
description: Select the simplest data types that satisfy requirements when designing
  API signatures. Avoid using complex types (like cty.Value) when simpler types (like
  string, int, bool) would suffice. This improves API usability, reduces complexity,
  and simplifies client implementations while maintaining consistent patterns across
  the API.
repository: hashicorp/terraform
label: API
language: Go
comments_count: 4
repository_stars: 45532
---

Select the simplest data types that satisfy requirements when designing API signatures. Avoid using complex types (like cty.Value) when simpler types (like string, int, bool) would suffice. This improves API usability, reduces complexity, and simplifies client implementations while maintaining consistent patterns across the API.

For example, prefer:
```go
type GetStatesResponse struct {
    // States is a list of state names
    States []string
}
```

Instead of:
```go
type GetStatesResponse struct {
    // States is a list of state names
    States []cty.Value
}
```

When extending existing APIs or adding new functionality, follow established naming and structural conventions to create a cohesive and predictable interface. Use helper functions provided by the API rather than reimplementing functionality, and ensure documentation accurately reflects method signatures, parameters, and return types to prevent confusion.