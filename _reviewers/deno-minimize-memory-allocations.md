---
title: minimize memory allocations
description: Identify and eliminate unnecessary memory allocations in performance-critical
  code paths. This includes pre-allocating collections when the size is known, using
  static strings for common values, and avoiding intermediate data structures.
repository: denoland/deno
label: Performance Optimization
language: Rust
comments_count: 9
repository_stars: 103714
---

Identify and eliminate unnecessary memory allocations in performance-critical code paths. This includes pre-allocating collections when the size is known, using static strings for common values, and avoiding intermediate data structures.

Key strategies:
- **Pre-allocate collections**: When you know the expected size, pre-allocate vectors and hashmaps to avoid repeated reallocations
- **Use static strings**: For common values like HTTP methods, use `Cow::Borrowed` or `FastStaticString` instead of allocating new strings
- **Eliminate intermediate collections**: Avoid creating temporary data structures when you can process data in a single pass
- **Reuse attribute objects**: Cache and reuse expensive-to-create objects rather than recreating them

Example from HTTP method handling:
```rust
// Instead of always allocating:
fn method_slow(method: &http::Method) -> String {
    method.to_string()  // Always allocates
}

// Use static strings for common cases:
fn method_fast(method: &http::Method) -> Cow<'static, str> {
    match *method {
        Method::GET => Cow::Borrowed("GET"),
        Method::POST => Cow::Borrowed("POST"),
        // ... other common methods
        _ => Cow::Owned(method.to_string()),
    }
}
```

This optimization is particularly important in hot code paths where even small allocations can compound into significant performance overhead. Always measure the impact, as the complexity trade-off should be justified by measurable performance gains.