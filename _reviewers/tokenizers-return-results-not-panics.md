---
title: Return results not panics
description: Libraries should never panic as this can crash applications using the
  library. Always return a `Result` type rather than using functions or methods that
  can panic (`panic!()`, `unwrap()`, `expect()`, `assert!()`) in public APIs and internal
  logic. This allows consumers of your library to properly handle error conditions.
repository: huggingface/tokenizers
label: Error Handling
language: Rust
comments_count: 8
repository_stars: 9868
---

Libraries should never panic as this can crash applications using the library. Always return a `Result` type rather than using functions or methods that can panic (`panic!()`, `unwrap()`, `expect()`, `assert!()`) in public APIs and internal logic. This allows consumers of your library to properly handle error conditions.

For example, instead of:
```rust
// BAD: This will panic if the string doesn't match any scheme
impl From<&str> for PrependScheme {
    fn from(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "first" => PrependScheme::First,
            "never" => PrependScheme::Never,
            "always" => PrependScheme::Always,
            _ => panic!("Invalid value for PrependScheme: {}", s),
        }
    }
}
```

Prefer:
```rust
// GOOD: Returns Result so the caller can handle the error
impl TryFrom<&str> for PrependScheme {
    type Error = String;
    
    fn try_from(s: &str) -> Result<Self, Self::Error> {
        match s.to_lowercase().as_str() {
            "first" => Ok(PrependScheme::First),
            "never" => Ok(PrependScheme::Never),
            "always" => Ok(PrependScheme::Always),
            _ => Err(format!("Invalid value for PrependScheme: {}", s)),
        }
    }
}
```

Similarly, instead of using `.unwrap()` or `.expect()` on `Option`s or `Result`s, propagate errors up the call stack. For public APIs that are expected to succeed under normal circumstances, validate inputs and return informative errors rather than using assertions.

When handling regex matches or other operations that theoretically shouldn't fail but might in practice, return appropriate error types rather than assuming success with `.expect()`. This approach makes your library more robust and provides a better experience for users.