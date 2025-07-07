---
title: Prefer explicit API design
description: When designing APIs, favor simple and explicit interfaces over flexible
  but complex ones. This reduces cognitive load, improves compile-time checking, and
  makes the code more maintainable.
repository: huggingface/tokenizers
label: API
language: Rust
comments_count: 4
repository_stars: 9868
---

When designing APIs, favor simple and explicit interfaces over flexible but complex ones. This reduces cognitive load, improves compile-time checking, and makes the code more maintainable.

Key principles:
1. Use concrete types instead of trait bounds when the use cases are limited
2. Split complex return types into separate methods rather than using variant returns
3. Group related parameters together instead of exposing them separately

Example - Instead of flexible but costly:
```rust
pub fn vocab<S: BuildHasher>(mut self, vocab: HashMap<String, u32, S>) -> Self {
    // Implementation
}
```

Prefer explicit:
```rust
pub fn vocab(mut self, vocab: HashMap<String, u32>) -> Self {
    // Implementation
}
```

Or when dealing with multiple return types, instead of:
```rust
fn token_to_word(token: usize) -> Option<(usize, usize)> | Option<usize> {
    // Implementation varies based on sequence count
}
```

Prefer separate methods:
```rust
fn token_to_word(token: usize) -> Option<usize> {
    // Single sequence implementation
}

fn token_to_word_with_sequence(token: usize) -> Option<(usize, usize)> {
    // Multi-sequence implementation
}
```

This approach makes APIs more predictable, easier to maintain, and reduces potential runtime errors by catching issues at compile-time.