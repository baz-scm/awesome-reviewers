---
title: Optimize hot paths
description: 'Identify and optimize frequently executed code paths to improve performance.
  Hot paths have a significant impact on overall application performance.


  Key strategies include:'
repository: tokio-rs/tokio
label: Performance Optimization
language: Rust
comments_count: 5
repository_stars: 28989
---

Identify and optimize frequently executed code paths to improve performance. Hot paths have a significant impact on overall application performance.

Key strategies include:

1. **Use inline attributes for small functions**: Add `#[inline]` to small functions called in performance-critical sections:
```rust
#[doc(hidden)]
#[inline]  // Added to improve inlining in hot paths
pub fn has_budget_remaining() -> bool {
    // Function body
}
```

2. **Implement early returns**: Avoid unnecessary computation when a quick result is possible:
```rust
pub fn poll_next_many(/* params */) -> Poll<usize> {
    if limit == 0 || self.entries.is_empty() {
        return Poll::Ready(0);  // Early return avoids unnecessary work
    }
    // Remaining logic
}
```

3. **Reduce lock contention**: Store frequently accessed constant data outside of locks:
```rust
// Instead of obtaining a lock to read a constant value
fn get_shard_size(&self) -> u32 {
    // Store this as a field instead of reading through a lock
    self.shard_count  // Direct field access instead of lock.read().len()
}
```

4. **Minimize atomic operations**: Evaluate whether atomic operations in hot paths can be avoided or optimized.

5. **Avoid generic code bloat**: Extract non-generic operations into separate functions to prevent monomorphization bloat, especially in frequently used code:
```rust
// Instead of using map with generic logic
impl::spawn_child_with(&mut self.std, with)  // Direct function call
```

Each optimization may seem small individually, but they can significantly improve performance when applied to code that executes thousands or millions of times.