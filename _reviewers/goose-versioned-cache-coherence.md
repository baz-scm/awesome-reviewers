---
title: Versioned cache coherence
description: When a cache is invalidated asynchronously, ensure *coherence* between
  (a) the invalidation/version signal and (b) the cached payload/derived artifacts.
repository: aaif-goose/goose
label: Caching
language: Rust
comments_count: 3
repository_stars: 51876
---

When a cache is invalidated asynchronously, ensure *coherence* between (a) the invalidation/version signal and (b) the cached payload/derived artifacts.

**Standard**
1. **Bundle version with payload**: design cache reads to return the version *alongside* the data they correspond to (e.g., `(version, tools)`). Never let callers read the version from one moment and the payload from another.
2. **Atomic invalidation under one lock**: when invalidating, update both the payload state and the version while holding the same synchronization/lock, so any observer of the new version cannot concurrently see stale payload.
3. **Refresh derived state immediately**: if your loop depends on cached data (e.g., tool lists used to build prompts), detect version changes and rebuild derived state using the newly returned `(version, payload)`—preferably in the same logical iteration/turn, not “some time later”.

**Illustrative pattern (Rust-like)**
```rust
// Cache stores version + payload together.
struct Cache<T> {
    inner: Option<(u64, T)>,
}

impl<T> Cache<T> {
    async fn get(&mut self, version: &AtomicU64, fetch: impl FnOnce() -> T) -> (u64, T) {
        if let Some((v, data)) = self.inner.as_ref().cloned() {
            return (v, data);
        }
        let v = version.load(Ordering::SeqCst);
        let data = fetch();
        self.inner = Some((v, data.clone()));
        (v, data)
    }

    async fn invalidate_and_bump(&mut self, version: &AtomicU64) {
        // Hold the lock for both operations.
        self.inner = None;
        version.fetch_add(1, Ordering::SeqCst);
    }
}

// Reply loop: baseline comes from the payload it used.
let (baseline_version, tools) = tools_cache.get(...).await;
// ... build prompts using `tools` ...
if extension_manager.tools_cache_version() != baseline_version {
    let (new_version, new_tools) = tools_cache.get(...).await;
    // Rebuild prompts derived from `new_tools`.
}
```

**Why**
- Separating “version reads” from “payload reads” allows drift during async notifications.
- Non-atomic invalidation allows observers to combine *new version* with *stale or empty payload*.

Adopting this standard prevents whole classes of intermittent “cache changed mid-use” bugs and makes refresh behavior deterministic under concurrency.