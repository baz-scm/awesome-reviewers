---
title: Graceful error handling
description: 'Prioritize graceful error handling over panicking by providing fallbacks
  and propagating rich context. When operations can fail:


  1. For non-critical failures, use fallbacks instead of unwrap():'
repository: tokio-rs/tokio
label: Error Handling
language: Rust
comments_count: 5
repository_stars: 28981
---

Prioritize graceful error handling over panicking by providing fallbacks and propagating rich context. When operations can fail:

1. For non-critical failures, use fallbacks instead of unwrap():
```rust
// Instead of this:
let pos = std.stream_position().unwrap();

// Prefer this:
let pos = std.stream_position().unwrap_or(0);
```

2. For functions that may panic with assertions, add `#[track_caller]` to improve error diagnostics:
```rust
#[track_caller]
pub fn global_queue_interval(&mut self, val: u32) -> &mut Self {
    assert!(val > 0, "global_queue_interval must be greater than 0");
    // ...
}
```

3. When exposing errors, implement the full `std::error::Error` trait including the `source()` method to maintain the error chain.

4. In documentation examples, demonstrate proper error handling rather than ignoring or silencing errors:
```rust
// Instead of ignoring errors:
let _ = compress_data(reader).await;

// Show proper error handling:
compress_data(reader).await?;
```

5. Consider providing configuration options for users to handle certain error conditions differently when appropriate.