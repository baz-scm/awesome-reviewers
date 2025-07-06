---
title: Minimize unsafe code
description: 'When writing code that requires unsafe operations, follow these critical
  security practices:


  1. Minimize the scope of unsafe blocks to only the specific operations that require
  them'
repository: tokio-rs/tokio
label: Security
language: Rust
comments_count: 3
repository_stars: 28981
---

When writing code that requires unsafe operations, follow these critical security practices:

1. Minimize the scope of unsafe blocks to only the specific operations that require them
2. Document each unsafe block with a `// SAFETY:` comment explaining why the operation is safe
3. Use separate unsafe blocks for distinct unsafe operations rather than one large block

These practices reduce the risk of memory safety issues and make code easier to audit for security vulnerabilities.

Example:
```rust
// BAD: Large unsafe block with multiple operations
unsafe {
    let block = self.head.as_ref();
    let tail_block = &mut *tail;
    // More code...
}

// GOOD: Minimal scope with documentation
// SAFETY: The tail pointer is guaranteed to be valid because...
let tail_block = unsafe { &mut *tail };

// More code with safe operations...
```

By limiting the scope of unsafe code, you make it easier to verify its correctness and maintain memory safety guarantees.