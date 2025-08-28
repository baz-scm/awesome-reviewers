---
title: avoid unnecessary Arc wrapping
description: Don't wrap atomic types in Arc unless you need to share ownership across
  multiple owners. Atomic types like AtomicBool, AtomicU64, etc. are already thread-safe
  and can be used directly in structs that will be wrapped in Arc at a higher level.
repository: cloudflare/workerd
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 6989
---

Don't wrap atomic types in Arc unless you need to share ownership across multiple owners. Atomic types like AtomicBool, AtomicU64, etc. are already thread-safe and can be used directly in structs that will be wrapped in Arc at a higher level.

Using Arc<AtomicBool> creates unnecessary indirection and allocation overhead when AtomicBool alone provides the required thread safety. The Arc should be applied at the struct level that contains the atomic field, not around individual atomic fields.

Example of the anti-pattern:
```rust
struct Impl {
    sender: mpsc::SyncSender<Vec<u8>>,
    write_shutdown: Arc<std::sync::atomic::AtomicBool>, // Unnecessary Arc
}
```

Preferred approach:
```rust
struct Impl {
    sender: mpsc::SyncSender<Vec<u8>>,
    write_shutdown: std::sync::atomic::AtomicBool, // Direct atomic type
}

// Wrap the entire struct in Arc when sharing is needed
let impl_instance = Arc::new(Impl::new(...));
```

This reduces memory overhead, eliminates unnecessary heap allocation, and simplifies the code while maintaining the same thread safety guarantees.