---
title: Handle nulls with Option
description: Use Rust's Option type and its methods effectively to handle nullable
  values. This improves code clarity and safety by making null cases explicit and
  leveraging the type system.
repository: astral-sh/ruff
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 40619
---

Use Rust's Option type and its methods effectively to handle nullable values. This improves code clarity and safety by making null cases explicit and leveraging the type system.

Key practices:
1. Prefer Option<T> over tuple/primitive returns for nullable values
2. Use appropriate Option methods:
   - unwrap_or_default() for default values
   - expect() with descriptive messages for cases that shouldn't be null
   - is_some_and() for conditional checks
3. Remove redundant null checks when Option already provides the safety

Example - Before:
```rust
// Using tuple return
fn is_pragma_comment(comment: &str) -> (bool, usize) {
    // Returns (is_pragma, offset)
    if comment.contains("pragma") {
        (true, comment.find("pragma").unwrap_or(0))
    } else {
        (false, 0)
    }
}
```

After:
```rust
// Using Option for clearer semantics
fn is_pragma_comment(comment: &str) -> Option<usize> {
    // Returns offset if comment is pragma, None otherwise
    comment.contains("pragma").then(|| {
        comment.find("pragma").expect("pragma exists")
    })
}

// Usage with appropriate Option methods
let offset = is_pragma_comment(comment)
    .unwrap_or_default();  // Use default when None
```

This approach:
- Makes null cases explicit in the type system
- Reduces error-prone manual null checking
- Provides clear, chainable operations for handling null cases
- Improves code readability and maintainability