---
title: avoid panics gracefully
description: Replace panic-prone operations like `unwrap()` and `expect()` with graceful
  error handling that provides meaningful feedback. When encountering unexpected conditions,
  prefer logging warnings and falling back to reasonable defaults rather than crashing
  the application.
repository: denoland/deno
label: Error Handling
language: Rust
comments_count: 5
repository_stars: 103714
---

Replace panic-prone operations like `unwrap()` and `expect()` with graceful error handling that provides meaningful feedback. When encountering unexpected conditions, prefer logging warnings and falling back to reasonable defaults rather than crashing the application.

Key practices:
- Replace `unwrap()` with proper error handling and user-friendly messages
- Use `expect()` only when the panic condition truly should never occur
- Implement fallback mechanisms when primary operations fail
- Log warnings for unexpected but recoverable errors
- Handle edge cases like binary files or missing data gracefully

Example transformation:
```rust
// Avoid this - can panic on unexpected input
let path = output.canonicalize().unwrap().to_string_lossy().to_string();

// Prefer this - graceful error handling
let path = match output.canonicalize() {
    Ok(path) => path.to_string_lossy().to_string(),
    Err(err) => {
        eprintln!("Failed to canonicalize path: {}", err);
        return Err(err);
    }
};
```

This approach prevents application crashes from unexpected conditions while still providing useful diagnostic information for debugging and user feedback.