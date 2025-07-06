---
title: Avoid flaky test patterns
description: 'Write reliable tests by avoiding common patterns that can lead to flaky
  behavior. Specifically:


  1. Avoid arbitrary timeouts and sleeps in tests. Instead, use proper test infrastructure
  or wait for specific conditions.'
repository: influxdata/influxdb
label: Testing
language: Rust
comments_count: 4
repository_stars: 30268
---

Write reliable tests by avoiding common patterns that can lead to flaky behavior. Specifically:

1. Avoid arbitrary timeouts and sleeps in tests. Instead, use proper test infrastructure or wait for specific conditions.
2. Don't rely on snapshot testing for non-deterministic data like serialized maps.
3. Use proper test abstractions rather than low-level timing controls.

Example of problematic code:
```rust
#[test]
async fn test_telemetry() {
    let store = TelemetryStore::new().await;
    tokio::time::sleep(Duration::from_secs(1)).await; // Flaky!
    assert!(store.duration > 0);
}
```

Better approach:
```rust
#[test]
async fn test_telemetry() {
    let store = TelemetryStore::new().await;
    // Use TestServer or similar infrastructure
    let server = TestServer::spawn().await;  // Waits for actual readiness
    assert!(store.is_ready());
    // Or implement explicit condition checking
    wait_for_condition(|| store.duration > 0, "store duration").await;
}
```

For serialization testing, prefer explicit equality checks over snapshot comparisons when dealing with non-deterministic data structures.