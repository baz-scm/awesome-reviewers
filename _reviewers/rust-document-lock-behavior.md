---
title: Document lock behavior
description: When implementing or documenting synchronization primitives, always clearly
  specify how locks behave under exceptional conditions, particularly during thread
  panics. This information is critical for developers to write robust concurrent code.
repository: rust-lang/rust
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 105254
---

When implementing or documenting synchronization primitives, always clearly specify how locks behave under exceptional conditions, particularly during thread panics. This information is critical for developers to write robust concurrent code.

Key aspects to document:
1. What happens to the lock when a thread holding it panics
2. How other threads can interact with previously locked resources
3. Whether the implementation uses poisoning or non-poisoning semantics

For example, when documenting a mutex implementation, include explicit statements like:

```rust
/// If this thread panics while the lock is held, the lock will be released like normal.
/// 
/// # Example
/// 
/// ```rust
/// use std::thread;
/// use std::sync::{Arc, nonpoison::Mutex};
/// 
/// let mutex = Arc::new(Mutex::new(0u32));
/// let mut handles = Vec::new();
/// 
/// for n in 0..10 {
///     let m = Arc::clone(&mutex);
///     let handle = thread::spawn(move || {
///         let mut guard = m.lock();
///         *guard += 1;
///         panic!("panic from thread {n} {guard}")
///     });
///     handles.push(handle);
/// }
/// 
/// for h in handles {
///     h.join().unwrap_err(); // Threads panicked as expected
/// }
/// 
/// // The mutex can still be locked despite previous panics
/// println!("Finished, locked {} times", mutex.lock());
/// ```
///
```

Additionally, be explicit about concurrent operation limits and clearly distinguish between different types of memory operations (e.g., volatile vs. atomic) to prevent misuse in concurrent contexts.