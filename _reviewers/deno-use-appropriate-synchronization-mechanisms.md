---
title: Use appropriate synchronization mechanisms
description: Select and implement synchronization primitives that match your concurrency
  requirements and avoid unsafe patterns. Consider the number of consumers, thread
  safety requirements, and proper initialization order.
repository: denoland/deno
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 103714
---

Select and implement synchronization primitives that match your concurrency requirements and avoid unsafe patterns. Consider the number of consumers, thread safety requirements, and proper initialization order.

Key guidelines:
- Avoid environment variable modification (`std::env::set_var`, `std::env::remove_var`) in multi-threaded programs as it can cause data races with C/C++ code
- Choose channel types based on usage patterns: use `broadcast` channels for multiple consumers, `mpsc` for single consumers
- Use proper synchronization primitives like conditional variables instead of polling loops for thread coordination
- Implement async flags and initialization correctly to prevent race conditions and out-of-order execution

Example of correct async flag implementation:
```rust
impl AsyncFlag {
  pub fn raise(&self) {
    self.0.add_permits(1);  // Preserve semaphore state
  }

  pub async fn wait_raised(&self) {
    drop(self.0.acquire().await);  // Proper waiting mechanism
  }
}
```

Avoid unsafe patterns like direct environment modification in multi-threaded contexts, and ensure synchronization primitives maintain proper ordering and state consistency throughout their lifecycle.