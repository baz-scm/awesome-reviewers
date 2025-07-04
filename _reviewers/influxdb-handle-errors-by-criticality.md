---
title: Handle errors by criticality
description: "Choose error handling strategies based on operation criticality:\n\n\
  1. For critical operations that could corrupt data or state:\n   - Use assertions/panics\
  \ to fail fast"
repository: influxdata/influxdb
label: Error Handling
language: Rust
comments_count: 5
repository_stars: 30268
---

Choose error handling strategies based on operation criticality:

1. For critical operations that could corrupt data or state:
   - Use assertions/panics to fail fast
   - Example: Validating snapshot details before WAL deletion
```rust
// Critical operation - use assert
assert_eq!(snapshot_details, details, 
    "Snapshot mismatch before WAL deletion");
```

2. For recoverable operations:
   - Return Result/Error types
   - Implement retry with backpressure
   - Log appropriately (warn for temporary, error for persistent issues)
```rust
// Recoverable operation - return Result
async fn persist_data(&self) -> Result<(), Error> {
    loop {
        match self.try_persist().await {
            Ok(_) => return Ok(()),
            Err(e) => {
                warn!("Temporary persist error, retrying: {}", e);
                tokio::time::sleep(Duration::from_secs(1)).await;
            }
        }
    }
}
```

3. For race conditions and invariant violations:
   - Use panic/assert when they indicate programming errors
   - Return errors when they represent expected edge cases

This approach ensures critical errors fail fast while allowing recovery from transient failures.