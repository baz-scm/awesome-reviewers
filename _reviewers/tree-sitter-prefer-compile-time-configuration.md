---
title: prefer compile-time configuration
description: Use compile-time configuration checks with `cfg!` macros instead of runtime
  environment variable parsing when the configuration decision can be determined at
  build time. This improves performance by eliminating runtime checks and makes the
  code's behavior more predictable.
repository: tree-sitter/tree-sitter
label: Configurations
language: Rust
comments_count: 7
repository_stars: 21799
---

Use compile-time configuration checks with `cfg!` macros instead of runtime environment variable parsing when the configuration decision can be determined at build time. This improves performance by eliminating runtime checks and makes the code's behavior more predictable.

**Prefer this:**
```rust
if cfg!(target_family = "wasm") {
    let sysroot = std::path::Path::new("bindings/rust/wasm-sysroot");
    c_config.include(sysroot);
}

#[cfg(target_env = "msvc")]
c_config.flag("-utf-8");

#[cfg(feature = "std")]
use std::fs;
```

**Instead of this:**
```rust
if std::env::var("TARGET").unwrap() == "wasm32-unknown-unknown" {
    let sysroot_dir = std::path::Path::new("bindings/rust/wasm-sysroot");
    c_config.include(sysroot_dir);
}
```

Use `cfg!` for target platform checks, `#[cfg(feature = "...")]` for optional features, and `#[cfg(target_env = "...")]` for toolchain-specific behavior. Reserve runtime environment variable checks for user-configurable settings that must be determined at runtime, not build-time architectural decisions.