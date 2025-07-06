---
title: Structural configuration approaches
description: When working with feature flags and conditional compilation, prefer structural
  approaches over scattered configuration attributes throughout your code. This creates
  more maintainable code and reduces the chance of bugs when features are added or
  removed.
repository: tokio-rs/tokio
label: Configurations
language: Rust
comments_count: 6
repository_stars: 28989
---

When working with feature flags and conditional compilation, prefer structural approaches over scattered configuration attributes throughout your code. This creates more maintainable code and reduces the chance of bugs when features are added or removed.

For conditionally included parameters:
```rust
// AVOID: Using cfg directly on function parameters
fn spawn(
    &mut self,
    task: T,
    scheduler: S,
    id: super::Id,
    #[cfg(tokio_unstable)] spawned_at: &'static Location<'static>,
) { /* ... */ }

// PREFER: Wrapping conditional data in a struct
struct SpawnLocation {
    #[cfg(tokio_unstable)]
    location: Option<&'static Location<'static>>,
    // The struct is effectively zero-sized when the feature is disabled
}

fn spawn(
    &mut self,
    task: T,
    scheduler: S,
    id: super::Id,
    location: SpawnLocation,
) { /* ... */ }
```

For platform-specific implementations:
```rust
// AVOID: Scattered cfg blocks within functions
fn now() {
    #[cfg(target_family = "wasm")]
    { return None; }
    #[cfg(not(target_family = "wasm"))]
    { return Some(Instant::now()); }
}

// PREFER: Abstraction functions that handle conditional logic
fn now() -> Option<Instant> {
    if cfg!(target_family = "wasm") { None } else { Some(Instant::now()) }
}
```

For feature-gated functionality, prefer separate function implementations over conditionally compiled code blocks:
```rust
// AVOID: Mixed conditional blocks within function bodies
fn submit(&mut self, worker: &WorkerMetrics, mean_poll_time: u64) {
    #[cfg(tokio_unstable)]
    {
        // unstable metrics code...
    }
    // stable metrics code...
}

// PREFER: Separate implementations with a common pattern
cfg_unstable_metrics! {
    fn submit_unstable(&mut self, worker: &WorkerMetrics, mean_poll_time: u64) {
        // unstable metrics code...
    }
}

fn submit(&mut self, worker: &WorkerMetrics, mean_poll_time: u64) {
    // stable metrics code...
    #[cfg(tokio_unstable)]
    self.submit_unstable(worker, mean_poll_time);
}
```

Consider creating specialized macros for common conditional patterns to standardize your approach:
```rust
// For metrics that have both stable and unstable implementations
macro_rules! cfg_metrics_impl {
    ($name:ident, stable: $stable_impl:block, unstable: $unstable_impl:block) => {
        cfg_unstable_metrics! {
            fn $name(&mut self) $unstable_impl
        }
        cfg_not_unstable_metrics! {
            fn $name(&mut self) $stable_impl
        }
    }
}
```

These structural approaches make conditional code easier to maintain, test, and understand.