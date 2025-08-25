---
title: Conditional telemetry flushing
description: Avoid fixed delays for telemetry flushing. Instead, make flushing conditional
  on whether telemetry endpoints are configured and use dynamic timeouts when possible.
repository: block/goose
label: Observability
language: Rust
comments_count: 2
repository_stars: 19037
---

Avoid fixed delays for telemetry flushing. Instead, make flushing conditional on whether telemetry endpoints are configured and use dynamic timeouts when possible.

Fixed sleep durations for telemetry flushing create unnecessary delays when no telemetry is configured and don't guarantee actual completion of data export. This is particularly problematic in CLI tools where delays accumulate across multiple runs.

**Implementation approach:**
1. Check if telemetry endpoints are configured before adding any delays
2. Consolidate multiple fixed sleeps into a single, centralized flushing mechanism
3. Use dynamic checks with maximum timeouts when the SDK supports it

**Example:**
```rust
// Instead of fixed delays everywhere:
tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
std::thread::sleep(std::time::Duration::from_millis(500));

// Use conditional flushing:
let should_flush = std::env::var("OTEL_EXPORTER_OTLP_ENDPOINT").is_ok()
    || config.get_param::<String>("otel_exporter_otlp_endpoint").is_ok();

if should_flush {
    shutdown_otlp_with_timeout(Duration::from_secs(2)).await;
}
```

This approach improves performance for users without telemetry configured while ensuring proper cleanup when telemetry is enabled.