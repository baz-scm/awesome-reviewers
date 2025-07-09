---
title: Proper Option type usage
description: Use Option<T> only for truly optional values that can meaningfully be
  None. Avoid using Option when a value is always required or when defaulting to empty/invalid
  values.
repository: neondatabase/neon
label: Null Handling
language: Rust
comments_count: 4
repository_stars: 19015
---

Use Option<T> only for truly optional values that can meaningfully be None. Avoid using Option when a value is always required or when defaulting to empty/invalid values.

Key guidelines:
1. Use Option<T> when a value may legitimately be absent
2. Avoid Option if a field is never None in practice
3. Don't use empty/default values as substitutes for Option<T>

Example:
```rust
// Good: Truly optional value
struct Config {
    refresh_interval: Option<Duration>,  // May not be configured
    error_message: Option<String>        // Only present on error
}

// Bad: Using Option when value is never None
struct AuthInterceptor {
    tenant_id: AsciiMetadataValue,
    shard_id: Option<AsciiMetadataValue>  // If always present, remove Option
}

// Bad: Using empty string instead of Option
struct Settings {
    base_url: String  // Empty string is meaningless, use Option<String>
}
```