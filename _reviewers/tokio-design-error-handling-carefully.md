---
title: Design error handling carefully
description: When implementing error handling, balance between propagation and recovery.
  Design error types to preserve context while providing users with meaningful ways
  to handle failure.
repository: tokio-rs/tokio
label: Error Handling
language: Rust
comments_count: 6
repository_stars: 28989
---

When implementing error handling, balance between propagation and recovery. Design error types to preserve context while providing users with meaningful ways to handle failure.

For error propagation:
- Implement the complete `std::error::Error` trait, including `source()` method for error chaining
- Choose return types that preserve necessary context (e.g., prefer `Result<usize>` over `Result<()>` when position information is needed)
- Use `Send + Sync` error types when errors might cross thread boundaries

For recovery paths:
- Provide fallback values for non-critical failures instead of panicking
- Simplify error variants when distinctions aren't meaningful to users

```rust
// Poor: May panic unexpectedly and loses context
let pos = std.stream_position().unwrap();

// Better: Provides fallback and preserves error context
let pos = std.stream_position().unwrap_or(0);

// Poor: Error type lacks context and proper trait implementation
struct MyError(());

// Better: Full featured error with context preservation
struct MyError<T> {
    inner: T,
    cause: io::Error,
}

impl<T> std::error::Error for MyError<T> {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.cause)
    }
}

// Even in examples, show proper error handling
// Poor: Ignores errors
let _ = compress_data(reader).await;

// Better: Shows proper error handling
compress_data(reader).await?;
```