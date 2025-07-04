---
title: Structure conditional compilation
description: 'Use organized structural patterns for conditional compilation to improve
  code maintainability and readability. Avoid applying `#[cfg]` attributes directly
  to function parameters - instead wrap conditionally available data in structs that
  can be zero-sized when features are disabled:'
repository: tokio-rs/tokio
label: Configurations
language: Rust
comments_count: 7
repository_stars: 28981
---

Use organized structural patterns for conditional compilation to improve code maintainability and readability. Avoid applying `#[cfg]` attributes directly to function parameters - instead wrap conditionally available data in structs that can be zero-sized when features are disabled:

```rust
// Instead of this:
fn function(
    param1: Type1,
    #[cfg(some_feature)] param2: Type2,
) {
    // ...
}

// Use this:
struct ConditionalParams {
    #[cfg(some_feature)]
    param2: Type2,
}

fn function(
    param1: Type1,
    conditional: ConditionalParams,
) {
    // ...
}
```

For functions with different implementations based on configuration, use macro blocks to separate complete implementations rather than conditionally compiling within function bodies:

```rust
cfg_feature! {
    fn my_function() {
        // Implementation when feature is enabled
    }
}

cfg_not_feature! {
    fn my_function() {
        // Implementation when feature is disabled
    }
}
```

When stabilizing features gradually, split implementations into stable and unstable parts to avoid duplication and potential divergence. Group all related unstable functions within a single configuration block. Prefer established configuration macros like `cfg_coop` over direct feature checks when they more accurately represent the conditions for enabling functionality.