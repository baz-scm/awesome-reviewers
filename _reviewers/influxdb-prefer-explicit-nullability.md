---
title: Prefer explicit nullability
description: Always make nullable states explicit in your code by leveraging Rust's
  type system. Use `Option<T>` rather than sentinel values (like empty structs or
  default values) to represent potentially missing data. When handling options, prefer
  idiomatic patterns like `.map()` with `.unwrap_or()` for transforming with fallbacks.
  Consider specialized types like...
repository: influxdata/influxdb
label: Null Handling
language: Rust
comments_count: 5
repository_stars: 30268
---

Always make nullable states explicit in your code by leveraging Rust's type system. Use `Option<T>` rather than sentinel values (like empty structs or default values) to represent potentially missing data. When handling options, prefer idiomatic patterns like `.map()` with `.unwrap_or()` for transforming with fallbacks. Consider specialized types like `NonZeroUsize` when values should never be null or zero.

```rust
// Good: Return Option<PathBuf> instead of empty PathBuf
fn find_python_install() -> Option<PathBuf> {
    // Return Some(path) when found, None otherwise
}

// Good: Idiomatic handling of nullable values
snap.retention_period
    .map(Snapshot::from_snapshot)
    .unwrap_or(RetentionPeriod::Indefinite)

// Good: Using specialized non-null type
#[derive(Debug, Serialize, Eq, PartialEq, Clone, Copy)]
pub struct LastCacheSize(pub(crate) NonZeroUsize);

// Good: Explicit null representation in data structures
struct LastCacheKey {
    column_name: String,
    value_map: HashMap<Option<KeyValue>, LastCacheState>
}
```

When working with external libraries like Arrow, use appropriate null-checking methods (e.g., `is_valid()`) and handle null values consistently rather than treating them as error conditions.