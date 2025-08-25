---
title: avoid panics and expects
description: Replace panic-inducing operations like `.expect()` and `.unwrap()` with
  proper error handling that allows graceful recovery or controlled failure. Panics
  can crash entire applications and provide poor user experience, especially in server
  environments where "it will kill goosed and it is all over."
repository: block/goose
label: Error Handling
language: Rust
comments_count: 6
repository_stars: 19037
---

Replace panic-inducing operations like `.expect()` and `.unwrap()` with proper error handling that allows graceful recovery or controlled failure. Panics can crash entire applications and provide poor user experience, especially in server environments where "it will kill goosed and it is all over."

Instead of panicking, use Result types, `.ok_or()` methods, or provide sensible defaults:

```rust
// Instead of panicking:
let stderr = stderr.take().expect("should have a stderr handle");

// Use proper error handling:
let stderr = stderr.take().ok_or_else(|| 
    ExtensionError::ConfigError("Missing stderr handle".to_string()))?;

// Or provide defaults when appropriate:
fn get_current_working_dir() -> PathBuf {
    std::env::current_dir()
        .unwrap_or_else(|_| get_home_dir())
}
```

When encountering unexpected None values or potential failures, log the issue and either return an appropriate error or continue with a reasonable fallback. This approach makes applications more resilient and provides better debugging information when issues occur.