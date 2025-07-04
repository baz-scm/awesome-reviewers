---
title: Design flexible APIs
description: When designing APIs, prioritize flexibility, ergonomics, and intuitiveness
  to create better user experiences. APIs should accept the most general parameter
  types appropriate for the functionality, handle edge cases gracefully, and provide
  methods that align with user expectations.
repository: tokio-rs/tokio
label: API
language: Rust
comments_count: 5
repository_stars: 28981
---

When designing APIs, prioritize flexibility, ergonomics, and intuitiveness to create better user experiences. APIs should accept the most general parameter types appropriate for the functionality, handle edge cases gracefully, and provide methods that align with user expectations.

Key practices:
1. Accept general parameter types (e.g., `impl Into<String>` instead of `String`)
2. For asynchronous operations, consider returning values directly from awaited functions
3. Provide inspection methods that allow users to query object state
4. Handle edge cases explicitly in your API design

Example of flexible parameter types:
```rust
// Instead of this:
pub fn name(&mut self, name: String) -> &mut Self {
    // implementation
}

// Prefer this:
pub fn name(&mut self, name: impl Into<String>) -> &mut Self {
    let name = name.into();
    // implementation
}
```

Example of intuitive async API design:
```rust
// Instead of requiring separate calls:
pub async fn wait(&self) {
    // implementation that just waits
}
pub fn get(&self) -> Option<&T> {
    // implementation
}

// Consider this more ergonomic design:
pub async fn wait(&self) -> &T {
    // implementation that returns the value directly
}
```

Example of providing inspection methods:
```rust
impl<T> Receiver<T> {
    /// Checks if this receiver is finished.
    ///
    /// Returns true if this receiver has been polled and yielded a result.
    pub fn is_finished(&self) -> bool {
        self.inner.is_none()
    }
    
    // Additional inspection methods to query other aspects of state
}
```