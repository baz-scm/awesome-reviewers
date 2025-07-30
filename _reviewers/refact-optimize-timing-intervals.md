---
title: optimize timing intervals
description: Choose appropriate timing intervals for asynchronous operations to improve
  performance and responsiveness. For frequent polling of cheap operations, use shorter
  intervals (200ms instead of 1s) to reduce latency. For potentially blocking file
  system operations, use atomic patterns like rename-then-delete to avoid blocking
  the async runtime.
repository: smallcloudai/refact
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 3114
---

Choose appropriate timing intervals for asynchronous operations to improve performance and responsiveness. For frequent polling of cheap operations, use shorter intervals (200ms instead of 1s) to reduce latency. For potentially blocking file system operations, use atomic patterns like rename-then-delete to avoid blocking the async runtime.

Example of optimized polling:
```rust
// Instead of 1-second polling
tokio::time::sleep(Duration::from_secs(1)).await;

// Use shorter intervals for cheap status checks
tokio::time::sleep(Duration::from_millis(200)).await;
```

Example of non-blocking file operations:
```rust
// Instead of direct removal that can block
tokio::fs::remove_dir_all(&path).await;

// Use atomic rename then remove pattern
let temp_path = path.with_extension("to-remove");
tokio::fs::rename(&path, &temp_path).await?;
tokio::fs::remove_dir_all(&temp_path).await;
```

This approach reduces unnecessary waiting time for responsive operations while preventing blocking operations from degrading overall system performance.