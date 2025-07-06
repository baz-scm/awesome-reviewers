---
title: Choose appropriate lock primitives
description: Select lock types based on access patterns - prefer RWLock over Mutex
  for read-heavy operations to enable concurrent reads while allowing exclusive write
  access. Minimize lock scope to essential operations and avoid holding locks across
  await points in async code.
repository: influxdata/influxdb
label: Concurrency
language: Rust
comments_count: 8
repository_stars: 30268
---

Select lock types based on access patterns - prefer RWLock over Mutex for read-heavy operations to enable concurrent reads while allowing exclusive write access. Minimize lock scope to essential operations and avoid holding locks across await points in async code.

```rust
// AVOID: Using Mutex for read-heavy operations
type MetaData = Mutex<HashMap<String, HashMap<String, ParquetFile>>>; 

// BETTER: Using RWLock for read-heavy operations
type MetaData = RwLock<HashMap<String, HashMap<String, ParquetFile>>>;

// AVOID: Taking lock before doing computation
async fn persist_parquet_file(&self) -> Result<(), Error> {
    // Lock held during entire function including computation
    let mut meta_data_lock = self.meta_data.write();
    // Long computation while holding lock
    let result = compute_expensive_result().await?;
    // Update metadata
}

// BETTER: Taking lock only when needed
async fn persist_parquet_file(&self) -> Result<(), Error> {
    // Do computation without holding lock
    let result = compute_expensive_result().await?;
    
    // Only take lock when updating shared state
    let mut meta_data_lock = self.meta_data.write();
    // Update metadata with minimal lock time
}
```

For high-contention scenarios, consider specialized concurrent data structures like DashMap that distribute lock contention. Keep related data under the same lock to ensure atomic updates across multiple data structures.