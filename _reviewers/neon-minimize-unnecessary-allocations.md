---
title: Minimize unnecessary allocations
description: 'Avoid allocations and cloning when they don''t provide sufficient benefit
  relative to their performance cost. Balance optimization efforts against code readability,
  especially in rarely executed paths. Specifically:'
repository: neondatabase/neon
label: Performance Optimization
language: Rust
comments_count: 6
repository_stars: 19015
---

Avoid allocations and cloning when they don't provide sufficient benefit relative to their performance cost. Balance optimization efforts against code readability, especially in rarely executed paths. Specifically:

1. Return static strings or use direct values instead of string formatting when possible
2. Avoid unnecessary `.clone()` calls on values that are already being moved
3. Prefer owned-type conversions over reference conversions to avoid implicit allocations
4. Use iterator combinators like `itertools::join` instead of collecting into intermediate collections
5. Avoid redundant cloning in asynchronous code paths

However, don't sacrifice code readability for minor optimizations that don't meaningfully impact performance:

```rust
// Prefer this when the code path is critical and frequently used:
pub fn v_str(&self) -> &'static str {
    match self {
        PgMajorVersion::PG17 => "v17",
        PgMajorVersion::PG16 => "v16",
        PgMajorVersion::PG15 => "v15",
        PgMajorVersion::PG14 => "v14",
    }
}

// But this might be acceptable for rarely executed code where simplicity matters more:
pub fn assemble_response(self) -> tonic::Result<page_api::GetPageResponse> {
    // Using a Vec allocation here is fine if it keeps the code simpler
    // and this is a rare code path with larger I/O costs elsewhere
    let mut response = page_api::GetPageResponse {
        page_images: Vec::with_capacity(self.block_shards.len()),
        // ... other fields
    };
    // ...
}
```

Focus your optimization efforts on frequently executed code paths where the performance gains outweigh the cost to code clarity.