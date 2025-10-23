---
title: optimize algorithmic complexity
description: Prioritize algorithmic efficiency by choosing operations and data structures
  that minimize computational complexity. Look for opportunities to replace O(n) operations
  with O(1) alternatives, select appropriate data structures for the use case, and
  avoid unnecessary algorithmic overhead.
repository: servo/servo
label: Algorithms
language: Rust
comments_count: 11
repository_stars: 32962
---

Prioritize algorithmic efficiency by choosing operations and data structures that minimize computational complexity. Look for opportunities to replace O(n) operations with O(1) alternatives, select appropriate data structures for the use case, and avoid unnecessary algorithmic overhead.

Key optimization strategies:
- **Replace traversals with direct access**: Instead of walking ancestor chains, provide O(1) root node access methods when possible
- **Choose efficient data structures**: Use FxHashMap for small keys and non-user-controlled data, but standard HashMap for user input to prevent hash collision attacks
- **Implement caching strategies**: Cache computed transformations and reuse buffers to avoid repeated expensive operations
- **Simplify control flow**: Use direct methods like `is_some_and()` and `if let` instead of complex nested operations

Example of complexity optimization:
```rust
// Instead of O(n) traversal:
fn get_root_slow(&self) -> Self {
    let mut current = self.clone();
    while let Some(parent) = current.parent() {
        current = parent;
    }
    current
}

// Provide O(1) direct access:
fn get_root_node(&self) -> Self {
    // Often possible to get root in O(1) if in shadow/document tree
    self.document().root_element()
}
```

This approach reduces computational overhead and improves performance, especially in frequently called code paths involving DOM traversal, data structure operations, and rendering algorithms.