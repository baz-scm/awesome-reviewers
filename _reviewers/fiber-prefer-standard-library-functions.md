---
title: Prefer standard library functions
description: When implementing algorithms, prioritize using standard library functions
  over manual implementations when they provide equivalent or better performance.
  The standard library is typically optimized and well-tested, making it a more reliable
  choice for common operations.
repository: gofiber/fiber
label: Algorithms
language: Go
comments_count: 3
repository_stars: 37560
---

When implementing algorithms, prioritize using standard library functions over manual implementations when they provide equivalent or better performance. The standard library is typically optimized and well-tested, making it a more reliable choice for common operations.

For example, instead of manually copying map entries:
```go
// Avoid manual iteration
for k, v := range m {
    c[k] = v
}

// Prefer standard library function
maps.Copy(c, m)
```

Similarly, for string operations, the standard library is often more efficient:
```go
// Use strings.ToLower() instead of custom utilities
origin := strings.ToLower(c.Get(fiber.HeaderOrigin))
```

This approach reduces code complexity, leverages optimized implementations, and improves maintainability. The standard library functions are particularly efficient when input data is already in the expected format, as noted: "standard lib is faster if it is already lower case, which should be the case in most cases."