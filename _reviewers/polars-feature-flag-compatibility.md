---
title: Feature flag compatibility
description: 'Design code to work correctly with any combination of feature flags.
  When implementing conditional compilation with feature flags:


  1. Use conditional imports for dependencies that are only needed when certain features
  are enabled:'
repository: pola-rs/polars
label: Configurations
language: Rust
comments_count: 3
repository_stars: 34296
---

Design code to work correctly with any combination of feature flags. When implementing conditional compilation with feature flags:

1. Use conditional imports for dependencies that are only needed when certain features are enabled:
```rust
// Good: Only import when feature is enabled
use polars_core::POOL;
#[cfg(feature = "new_streaming")]
use polars_core::StringCacheHolder;

// Bad: Requiring dependencies unconditionally
use polars_core::{POOL, StringCacheHolder};  // Breaks when "new_streaming" is disabled
```

2. Consider user scenarios with different feature combinations. Test both with and without features enabled.

3. Ensure error messages reference correct feature names:
```rust
// Good: Reference the correct feature name
polars_bail!(
    ComputeError: "consider compiling with polars-bigidx feature, or set 'streaming'"
)

// Bad: Referencing incorrect feature name
polars_bail!(
    ComputeError: "consider compiling with polars-u64-idx feature, or set 'streaming'"
)
```

4. When adding code conditionally compiled with feature flags, check that the code still compiles and functions correctly when those features are disabled.

5. Consider organizing feature-dependent code to minimize duplication while maintaining compatibility with all feature combinations.