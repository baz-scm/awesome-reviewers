---
title: Design metrics for insights
description: 'Design metrics that provide actionable insights while maintaining system
  efficiency. Follow these key principles:


  1. Track success and failure counts instead of just total counts to enable error
  rate calculations'
repository: neondatabase/neon
label: Observability
language: Rust
comments_count: 5
repository_stars: 19015
---

Design metrics that provide actionable insights while maintaining system efficiency. Follow these key principles:

1. Track success and failure counts instead of just total counts to enable error rate calculations
2. Consider cardinality impact when adding dimension labels
3. Ensure exactly-once metric increments
4. Initialize metrics with meaningful default values

Example:
```rust
// Good: Track success/failure separately
pub static OPERATION_SUCCESS: Counter = register_counter!(
    "operation_success_total",
    "Number of successful operations"
);
pub static OPERATION_FAILURES: Counter = register_counter!(
    "operation_failure_total",
    "Number of failed operations"
);

// Bad: High cardinality with too many labels
pub static REQUESTS: CounterVec = register_counter_vec!(
    "requests_total",
    "Request count",
    &["endpoint", "user_id", "session_id"] // Too many dimensions
);

// Good: Focused dimensions
pub static REQUESTS: CounterVec = register_counter_vec!(
    "requests_total",
    "Request count",
    &["endpoint", "status"] // Key dimensions only
);
```