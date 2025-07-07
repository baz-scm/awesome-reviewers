---
title: Avoid unsafe code
description: Prioritize memory safety and security over performance optimizations
  by avoiding unsafe code blocks, especially in libraries. Even when bounds are checked,
  unsafe code can introduce subtle security vulnerabilities and maintenance challenges.
  Prefer using safe Rust patterns and abstractions, even if it means a slight performance
  overhead (like an additional...
repository: huggingface/tokenizers
label: Security
language: Rust
comments_count: 1
repository_stars: 9868
---

Prioritize memory safety and security over performance optimizations by avoiding unsafe code blocks, especially in libraries. Even when bounds are checked, unsafe code can introduce subtle security vulnerabilities and maintenance challenges. Prefer using safe Rust patterns and abstractions, even if it means a slight performance overhead (like an additional clone operation).

Example:
```rust
// Avoid this approach
#[inline]
fn split_off_back<T>(vec: &mut Vec<T>, at: usize) -> Vec<T> {
    assert!(vec.len() >= at);
    let mut other = Vec::with_capacity(at);
    let left_over_len = vec.len() - at;
    let at_isize = at.try_into().unwrap();
    unsafe {
        // unsafe implementation
    }
}

// Prefer this safer approach
#[inline]
fn split_off_back<T: Clone>(vec: &mut Vec<T>, at: usize) -> Vec<T> {
    let other = vec[0..at].to_vec(); // Clone but safe
    vec.rotate_left(at);
    vec.truncate(vec.len() - at);
    other
}
```