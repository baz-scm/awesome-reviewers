---
title: Cache performance preservation
description: 'When implementing database failover or restart mechanisms, ensure performance
  consistency by preserving and prewarming caches. Database performance can significantly
  degrade after restarts due to cold caches (buffer pools, file system cache, query
  plan cache), especially for large workloads. '
repository: neondatabase/neon
label: Database
language: Markdown
comments_count: 3
repository_stars: 19015
---

When implementing database failover or restart mechanisms, ensure performance consistency by preserving and prewarming caches. Database performance can significantly degrade after restarts due to cold caches (buffer pools, file system cache, query plan cache), especially for large workloads. 

Implement a cache prewarming strategy:
1. Periodically persist cache state to external storage (e.g., S3)
2. During failover, load cache state into the new instance before accepting traffic
3. Ensure clean handover between primaries during failover with proper sequencing:
   - Avoid concurrent primaries on the same timeline
   - Complete promotion before routing traffic
   - Validate replay of all committed transactions

Example code for cache state persistence:
```rust
struct ComputeSpec {
    // ...existing fields
    
    /// Whether to do auto-prewarm at start
    pub lfc_auto_prewarm: bool,
    
    /// Interval in seconds for periodic cache dumps
    pub lfc_dump_interval_sec: Option<i32>
}

// In the cache manager
fn periodic_cache_dump() {
    if let Some(interval) = config.lfc_dump_interval_sec {
        schedule_task(Duration::from_secs(interval as u64), || {
            // Dump cache state to persistent storage
            store_cache_state_to_s3();
        });
    }
}
```

For read-heavy workloads, consider implementing hot secondaries that can handle read traffic while maintaining cache warmth, providing both scaling benefits and faster failover.