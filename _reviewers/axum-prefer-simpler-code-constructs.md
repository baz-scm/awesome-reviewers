---
title: "Prefer simpler code constructs"
description: "Always opt for simpler, more idiomatic code constructs over complex or verbose alternatives. This includes using built-in Rust patterns instead of manual implementations, leveraging pattern matching for cleaner control flow, using method chaining when it improves readability, and maintaining consistent formatting."
repository: "tokio-rs/axum"
label: "Code Style"
language: "Rust"
comments_count: 6
repository_stars: 22100
---

Always opt for simpler, more idiomatic code constructs over complex or verbose alternatives. This includes:

1. Using built-in Rust patterns instead of manual implementations:
```rust
// Instead of
.for_each(|(name, value)| {
    // ... implementation
});

// Prefer
for (name, value) in items {
    // ... implementation
}
```

2. Leveraging pattern matching for cleaner control flow:
```rust
// Instead of
let content_length = req.method().clone();
if content_length > N { ... }

// Prefer
match (content_length, req.method()) {
    (content_length, &(Method::GET | Method::HEAD)) => { ... }
}
```

3. Using method chaining when it improves readability:
```rust
// Instead of
cmd.arg("--body");
cmd.arg(body);

// Prefer
cmd.args(&["--body", body])
```

4. Maintaining consistent formatting:
- Group related imports together
- Avoid mixing inline and non-inline arguments
- Use consistent line wrapping in documentation

The goal is to write code that is easier to read, maintain, and reason about by leveraging Rust's built-in constructs and following consistent patterns.