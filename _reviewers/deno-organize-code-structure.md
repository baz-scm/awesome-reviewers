---
title: organize code structure
description: Maintain clean code organization by moving implementation details to
  appropriate locations, extracting reusable functionality, and keeping related code
  together. This improves maintainability and prevents bugs from poor encapsulation.
repository: denoland/deno
label: Code Style
language: Rust
comments_count: 10
repository_stars: 103714
---

Maintain clean code organization by moving implementation details to appropriate locations, extracting reusable functionality, and keeping related code together. This improves maintainability and prevents bugs from poor encapsulation.

Key practices:
- Move implementation details to dedicated modules (e.g., move esbuild utilities to `bundle/esbuild.rs`)
- Extract repeated patterns into reusable functions instead of duplicating code
- Keep struct definitions close to their implementations for better cohesion
- Use named struct fields instead of tuples for public APIs to improve clarity
- Maintain proper encapsulation by keeping internal details private
- Avoid code duplication by centralizing common utilities (e.g., export shared macros from `deno_core`)

Example of good organization:
```rust
// Instead of inline implementation details
pub async fn bundle() -> Result<(), AnyError> {
  // ... lots of esbuild setup code ...
}

// Extract to dedicated module
// bundle/esbuild.rs
pub async fn ensure_esbuild(...) -> Result<PathBuf, AnyError> {
  // esbuild-specific logic here
}

// bundle/mod.rs  
pub async fn bundle() -> Result<(), AnyError> {
  let esbuild_path = esbuild::ensure_esbuild(...).await?;
  // ... main bundling logic ...
}
```

This approach makes code easier to test, maintain, and understand by grouping related functionality and separating concerns.