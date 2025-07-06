---
title: Memory ordering needs justification
description: When using atomic operations, explicitly justify the choice of memory
  ordering. Each use of a memory ordering should be documented with a clear explanation
  of why that specific ordering is sufficient and safe.
repository: tokio-rs/tokio
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 28981
---

When using atomic operations, explicitly justify the choice of memory ordering. Each use of a memory ordering should be documented with a clear explanation of why that specific ordering is sufficient and safe.

Key guidelines:
- Use Relaxed for simple counters without synchronization needs
- Use Acquire/Release for establishing happens-before relationships
- Avoid mixing SeqCst with other orderings
- Document safety assumptions for weaker orderings

Example:
```rust
impl<T> Clone for Sender<T> {
    fn clone(&self) -> Self {
        // Relaxed is sufficient for incrementing the reference count
        // since no synchronization is needed - the sender is already
        // guaranteed to be valid when Clone is called
        self.shared.ref_count.fetch_add(1, Relaxed);
        Self { shared: self.shared.clone() }
    }
}

impl<T> Drop for Sender<T> {
    fn drop(&mut self) {
        // AcqRel ordering required for reference count decrement
        // to synchronize with other threads that may be checking
        // if this is the last sender
        if self.shared.ref_count.fetch_sub(1, AcqRel) == 1 {
            self.shared.close();
        }
    }
}
```