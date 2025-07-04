---
title: Performance-conscious metrics implementation
description: Implement metrics collection that is both comprehensive and minimally
  impactful on system performance. Design your metrics system to avoid creating bottlenecks
  in critical paths.
repository: influxdata/influxdb
label: Observability
language: Rust
comments_count: 4
repository_stars: 30268
---

Implement metrics collection that is both comprehensive and minimally impactful on system performance. Design your metrics system to avoid creating bottlenecks in critical paths.

Key principles:
1. **Avoid high-overhead operations in critical paths**: Don't spawn new tasks for each metric update in hot code paths.

```rust
// Avoid this:
tokio::spawn(async move {
    // Update metrics
});

// Prefer this:
store.add_write_metrics(num_lines, payload_size);
```

2. **Use appropriate buffer sizing** for telemetry channels based on expected throughput. For high-volume services, consider larger buffers (e.g., 10k) or direct counter updates instead of channels.

```rust
// Consider higher capacity for high-volume metrics
let (sender, receiver) = mpsc::channel(10_000);
```

3. **Track both success and failure metrics** for all critical operations to provide a complete picture of system behavior.

```rust
// Example counters for both successful and failed operations
const WRITE_LINES_TOTAL_NAME: &str = "influxdb_write_lines_total";
const WRITE_LINES_REJECTED_TOTAL_NAME: &str = "influxdb_write_lines_rejected_total";
```

4. **Ensure proper isolation of metrics** across components. When using multiple executors or processing paths, avoid sharing metric registries if they cause conflicts.

Remember that metrics collection should provide valuable insights without becoming a performance bottleneck itself.