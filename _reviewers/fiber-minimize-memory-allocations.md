---
title: minimize memory allocations
description: Prioritize reducing memory allocations and choosing efficient data structures
  to improve performance. Avoid unnecessary string/byte conversions, use maps for
  O(1) lookups instead of slices, and leverage compiler optimizations where possible.
repository: gofiber/fiber
label: Performance Optimization
language: Go
comments_count: 9
repository_stars: 37560
---

Prioritize reducing memory allocations and choosing efficient data structures to improve performance. Avoid unnecessary string/byte conversions, use maps for O(1) lookups instead of slices, and leverage compiler optimizations where possible.

Key strategies:
- Use `utils.EqualFold` instead of `utils.ToLower` for case-insensitive comparisons to avoid allocations
- Choose maps over slices for lookups: `map[int]bool` instead of `[]int` for O(1) performance
- Preallocate slices with appropriate capacity to avoid runtime growth
- Combine string operations to reduce allocations: `strings.ToLower(scheme + "://" + host)` instead of separate calls
- Leverage Go compiler optimizations for `[]byte` to `string` comparisons
- Use library-specific optimized functions like `fasthttp.ParseFloat` and `UnsafeBytes` when available

Example:
```go
// Inefficient - multiple allocations
if utils.ToLower(cookie.SameSite) == CookieSameSiteNoneMode {
    // process
}

// Efficient - no allocations  
if utils.EqualFold(cookie.SameSite, CookieSameSiteNoneMode) {
    // process
}

// Inefficient - O(n) lookup
var cacheableStatusCodes = []int{200, 203, 300, 301}
if slices.Contains(cacheableStatusCodes, status) { /* ... */ }

// Efficient - O(1) lookup
var cacheableStatusCodes = map[int]bool{200: true, 203: true, 300: true, 301: true}
if cacheableStatusCodes[status] { /* ... */ }
```