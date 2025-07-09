---
title: Configurable cache parameters
description: Cache configurations should be runtime-configurable rather than hardcoded,
  with support for dynamic resizing when configuration changes. This practice improves
  adaptability to varying workloads and environments without requiring service restarts.
repository: neondatabase/neon
label: Caching
language: Rust
comments_count: 3
repository_stars: 19015
---

Cache configurations should be runtime-configurable rather than hardcoded, with support for dynamic resizing when configuration changes. This practice improves adaptability to varying workloads and environments without requiring service restarts.

When implementing caches:

1. Define cache capacities as configurable parameters:
```rust
// Instead of this:
const REL_SIZE_CACHE_CAPACITY: usize = 1024;

// Do this:
#[derive(Debug, Clone, Deserialize)]
pub struct TenantConfig {
    pub relsize_snapshot_cache_capacity: usize,
    // other config parameters...
}
```

2. Implement handlers to resize caches when configuration changes:
```rust
fn tenant_conf_updated(&self, new_conf: TenantConfig) {
    // Update the cache capacity when config changes
    let mut cache = self.rel_size_cache.write().unwrap();
    cache.resize_capacity(new_conf.relsize_snapshot_cache_capacity);
}
```

3. Handle existing entries properly during cache operations to prevent memory leaks:
```rust
fn insert(&mut self, key: K, value: V) {
    if self.cache.contains_key(&key) {
        // Handle existing entry - consider evicting old entry, 
        // updating statistics, or queueing for cleanup
        self.deletion_queue.send(key.clone());
    }
    self.cache.insert(key, value);
}
```

This approach ensures that caches can be tuned for optimal performance based on actual usage patterns without service disruptions, and properly manages the lifecycle of cached entries.