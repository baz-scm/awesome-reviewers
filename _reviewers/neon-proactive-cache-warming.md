---
title: Proactive cache warming
description: Implement proactive cache warming strategies to minimize performance
  degradation after system restarts or during cold starts. Rather than waiting for
  normal workload patterns to gradually populate caches, actively prefetch and load
  likely-needed data into memory ahead of time.
repository: neondatabase/neon
label: Performance Optimization
language: Markdown
comments_count: 4
repository_stars: 19015
---

Implement proactive cache warming strategies to minimize performance degradation after system restarts or during cold starts. Rather than waiting for normal workload patterns to gradually populate caches, actively prefetch and load likely-needed data into memory ahead of time.

For optimal performance:

1. Identify critical cache contents that impact application performance (like LFC state in compute nodes)
2. Implement mechanisms to periodically persist cache state with appropriate frequency (balancing cost vs performance)
3. Add functionality to load this state during startup or in background threads
4. Consider cost-performance tradeoffs when designing the cache dump frequency

```rust
struct ComputeSpec {
    // Whether to do auto-prewarm at start or not
    pub lfc_auto_prewarm: bool,
    // Interval in seconds between automatic dumps of LFC state
    // Default to 300s (5 min) for reasonable cost/performance balance
    pub lfc_dump_interval_sec: Option<i32>
}

// When implementing prewarming:
// 1. Store raw metrics for accurate measurement
struct PrewarmState {
    pub status: PrewarmStatus,
    // Use absolute values instead of percentages
    pub pages_total: usize,
    pub pages_processed: usize,
    pub error: Option<String>
}
```

By proactively warming caches, you can reduce the performance impact of restarts and provide more consistent user experience, especially for large workloads where cold cache performance can be significantly degraded.