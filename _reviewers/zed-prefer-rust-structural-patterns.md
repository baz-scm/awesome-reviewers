---
title: Prefer Rust structural patterns
description: 'Use Rust''s structural patterns to write more idiomatic and maintainable
  code. This includes:


  1. Use early returns to reduce nesting:

  ```rust

  // Instead of'
repository: zed-industries/zed
label: Code Style
language: Rust
comments_count: 6
repository_stars: 62119
---

Use Rust's structural patterns to write more idiomatic and maintainable code. This includes:

1. Use early returns to reduce nesting:
```rust
// Instead of
if condition {
    if other_condition {
        // deep nesting
    }
} 

// Prefer
if !condition { return }
if !other_condition { return }
// main logic
```

2. Leverage pattern matching and destructuring:
```rust
// Instead of
let response = response.body_mut().read_to_end(&mut body).await?;
if response.status().is_success() {
    // handle success
}

// Prefer
let Some((buffer, buffer_position)) = self.buffer.read(cx)
    .text_anchor_for_position(position, cx) 
else { return };
```

3. Use Rust's type system effectively:
```rust
// Instead of
signature_help_task: Default::default(),

// Prefer
signature_help_task: None,
```

4. Utilize iterator combinators to flatten logic:
```rust
// Instead of
.get_diagnostics(server_id)
    .map(|diag| {
        diag.iter()
            .filter(...)
            .map(...)
            .collect()
    })

// Prefer
.get_diagnostics(server_id)
    .into_iter()
    .flat_map(...)
```

These patterns improve code readability, reduce complexity, and make the code more maintainable by leveraging Rust's built-in features effectively.