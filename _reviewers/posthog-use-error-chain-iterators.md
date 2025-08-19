---
title: Use error chain iterators
description: When traversing error chains in Rust, prefer using the `chain()` iterator
  method over manual source traversal with while loops. The `chain()` method provides
  a more idiomatic and readable approach to walking through error chains, eliminating
  the need for manual loop management and making the code more concise.
repository: PostHog/posthog
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 28460
---

When traversing error chains in Rust, prefer using the `chain()` iterator method over manual source traversal with while loops. The `chain()` method provides a more idiomatic and readable approach to walking through error chains, eliminating the need for manual loop management and making the code more concise.

Instead of manually iterating through error sources:
```rust
let mut source = error.source();
while let Some(err) = source {
    if let Some(rl) = err.downcast_ref::<RateLimitedError>() {
        return rl.retry_after;
    }
    source = err.source();
}
```

Use the iterator-based approach:
```rust
error
    .chain()
    .find_map(|e| e.downcast_ref::<RateLimitedError>())
    .and_then(|rl| rl.retry_after)
```

This pattern works well with other iterator methods like `any()`, `find()`, and `filter_map()` to create more expressive and maintainable error handling code.