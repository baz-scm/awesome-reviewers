---
title: Keep documentation purposefully minimal
description: 'Documentation should be concise, focused, and maintainable. Follow these
  principles:


  1. Keep examples short and demonstrate one concept at a time

  2. Avoid redundant documentation across related items'
repository: rust-lang/rust
label: Documentation
language: Rust
comments_count: 9
repository_stars: 105254
---

Documentation should be concise, focused, and maintainable. Follow these principles:

1. Keep examples short and demonstrate one concept at a time
2. Avoid redundant documentation across related items
3. Include maintenance notes (FIXME/TODO) with issue links for temporary documentation
4. Document fields and parameters clearly but briefly

Good example:
```rust
/// A mutex guard for accessing protected data.
/// 
/// See [`Mutex`] for more usage examples.
#[must_use = "if unused the Mutex will immediately unlock"]
pub struct MutexGuard<'a, T: ?Sized + 'a> {
    /// The underlying mutex reference
    lock: &'a Mutex<T>,
}
```

Problematic example:
```rust
/// A mutex guard for accessing protected data.
/// This implements RAII pattern for mutex locking.
/// When dropped, it automatically unlocks the mutex.
/// 
/// # Examples
/// 
/// ```
/// // Long example duplicating documentation from Mutex
/// let mutex = Mutex::new(0);
/// let guard = mutex.lock();
/// *guard = 2;
/// // Many more lines...
/// ```
pub struct MutexGuard<'a, T: ?Sized + 'a> {
    lock: &'a Mutex<T>, // Undocumented field
}
```