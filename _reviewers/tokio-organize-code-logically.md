---
title: Organize code logically
description: Group related code elements together with a consistent and logical structure.
  Place stable fields and functionality first, followed by conditional or unstable
  features.
repository: tokio-rs/tokio
label: Code Style
language: Rust
comments_count: 6
repository_stars: 28989
---

Group related code elements together with a consistent and logical structure. Place stable fields and functionality first, followed by conditional or unstable features.

For struct definitions:
```rust
#[derive(Debug, Default)]
pub(crate) struct WorkerMetrics {
    // Stable fields first
    busy_duration_total: AtomicU64,
    
    // Conditional fields after stable ones
    #[cfg(tokio_unstable)]
    park_count: AtomicU64,
    
    #[cfg(tokio_unstable)]
    mean_poll_time: AtomicU64,
    
    // ...more fields
}
```

For implementation blocks:
```rust
impl MetricsBatch {
    // Regular methods first
    pub(crate) fn submit(&mut self, worker: &WorkerMetrics) {
        worker.busy_duration_total.store(self.busy_duration_total, Relaxed);
        
        // Call separate method for unstable features
        self.submit_unstable(worker);
    }
    
    // Unstable methods grouped together at the bottom
    cfg_unstable_metrics! {
        fn submit_unstable(&mut self, worker: &WorkerMetrics) {
            // Implementation for unstable features
        }
    }
}
```

Keep implementation blocks manageable by splitting large code blocks into separate files, especially within macros where formatting tools don't work well. Consider exposing single-item modules as direct exports:

```rust
// Instead of this:
pub mod abort_on_drop;

// Do this:
mod abort_on_drop;
pub use abort_on_drop::AbortOnDropHandle;
```

When public types would clutter documentation, organize them into logical submodules.