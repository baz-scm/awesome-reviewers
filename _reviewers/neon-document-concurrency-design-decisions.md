---
title: Document concurrency design decisions
description: 'Always document key concurrency design decisions in code, including:

  1. Locking protocols and ordering between multiple locks

  2. Assumptions about data access patterns and thread safety'
repository: neondatabase/neon
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 19015
---

Always document key concurrency design decisions in code, including:
1. Locking protocols and ordering between multiple locks
2. Assumptions about data access patterns and thread safety
3. State transition guarantees and potential race conditions
4. Rationale for chosen concurrency primitives

Example:
```rust
/// The locking protocol for this struct is:
/// - `index` must be acquired before `inner`
/// - `inner` is append-only, so it is safe to:
///   * read and release `index` before locking and reading from `inner`
///   * write and release `inner` before locking and updating `index`
/// 
/// This avoids holding `index` locks across IO operations and is crucial 
/// for avoiding read tail latency.
pub struct ConcurrentStorage {
    index: RwLock<BTreeMap<Key, Value>>,
    inner: RwLock<InnerData>,
}
```

Clear documentation of concurrency decisions helps prevent subtle bugs, makes code more maintainable, and enables safe evolution of concurrent systems. When concurrent code lacks proper documentation, reviewers and maintainers must reverse-engineer the intended synchronization patterns, which is error-prone and time-consuming.