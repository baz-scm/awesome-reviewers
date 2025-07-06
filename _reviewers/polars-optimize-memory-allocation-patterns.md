---
title: Optimize memory allocation patterns
description: 'Minimize memory allocations and optimize allocation patterns to improve
  performance. Key practices:


  1. Pre-allocate collections with known sizes

  2. Avoid unnecessary intermediate allocations'
repository: pola-rs/polars
label: Performance Optimization
language: Rust
comments_count: 6
repository_stars: 34296
---

Minimize memory allocations and optimize allocation patterns to improve performance. Key practices:

1. Pre-allocate collections with known sizes
2. Avoid unnecessary intermediate allocations
3. Reuse allocated memory when possible
4. Use appropriate capacity reservations

Example - Before:
```rust
// Allocates new Vec for each row
result.try_push(Some(
    x.chunks_exact(element_size)
        .map(|val| T::cast_le(val))
        .collect::<Vec<_>>(),
));
```

Example - After:
```rust
// Pre-allocate with known capacity
let mut builder = make_builder(arr.dtype());
builder.reserve(output_length);

// Avoid intermediate allocations
result.try_push(
    x.chunks_exact(element_size)
        .map(|val| T::cast_le(val))
);
```

Benefits:
- Reduced memory churn
- Better performance through fewer allocations
- More predictable memory usage patterns
- Lower risk of allocation-related performance spikes