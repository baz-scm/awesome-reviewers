---
title: Thread-safe resource sharing
description: When sharing mutable data between threads, use the `Arc<RwLock<T>>` pattern
  to ensure thread safety. `Arc` provides thread-safe reference counting for sharing
  ownership across thread boundaries, while `RwLock` enables controlled mutation of
  the shared data.
repository: huggingface/tokenizers
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 9868
---

When sharing mutable data between threads, use the `Arc<RwLock<T>>` pattern to ensure thread safety. `Arc` provides thread-safe reference counting for sharing ownership across thread boundaries, while `RwLock` enables controlled mutation of the shared data.

This pattern is particularly important when:
- Working across language boundaries (like Rust/Python bindings)
- Sharing objects that might be accessed from different threads
- Needing to mutate data that is referenced in multiple places

```rust
// Instead of this (not thread-safe for mutation):
let model = Arc::new(MyModel::new());

// Use this pattern for thread-safe mutation:
let model = Arc::new(RwLock::new(MyModel::new()));

// Reading from the shared resource:
let data = model.read().unwrap().get_data();

// Writing to the shared resource:
model.write().unwrap().update_data();
```

When working with `RwLock`, `unwrap()` is generally acceptable for lock acquisition failures as they indicate a thread panic (unrecoverable state), but consider proper error handling in production code where appropriate. Remember that `RwLock` allows multiple simultaneous readers but only one writer, optimizing for read-heavy workloads.