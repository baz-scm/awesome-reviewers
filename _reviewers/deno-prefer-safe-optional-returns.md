---
title: prefer safe optional returns
description: When designing APIs and handling potentially missing or unavailable values,
  prefer returning optional types (Option<T>, Result<T, E>) over operations that can
  panic or fail unsafely. This promotes defensive programming and null safety.
repository: denoland/deno
label: Null Handling
language: Rust
comments_count: 4
repository_stars: 103714
---

When designing APIs and handling potentially missing or unavailable values, prefer returning optional types (Option<T>, Result<T, E>) over operations that can panic or fail unsafely. This promotes defensive programming and null safety.

Key practices:
- Return `None` instead of using `unreachable!()` for cases that might become reachable in the future
- Use `Option<T>` for platform-specific values that may not be available everywhere
- Handle errors explicitly rather than using `unwrap()` which can panic
- Avoid "rogue None" parameters by designing specialized APIs when possible

Example from the discussions:
```rust
// Instead of this (can panic if plugin changes):
_ => unreachable!(),

// Prefer this (safe fallback):
_ => None,

// For platform-specific values:
// Instead of: Result<(ResourceId, IpAddr, IpAddr, Fd), NetError>
// Use: Result<(ResourceId, IpAddr, IpAddr, Option<Fd>), NetError>

// Handle errors instead of panicking:
// Instead of: parsed_source.specifier().to_file_path().unwrap()
// Use proper error handling with Result types
```

This approach makes code more robust, prevents runtime panics, and clearly communicates when values might be absent through the type system.