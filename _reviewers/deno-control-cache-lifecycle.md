---
title: Control cache lifecycle
description: Design cache systems so that higher-level components control when cache
  entries are invalidated or cleaned up, rather than having cache operations happen
  automatically at lower levels. This allows callers to make informed decisions about
  cache lifecycle based on their broader context and requirements.
repository: denoland/deno
label: Caching
language: Rust
comments_count: 3
repository_stars: 103714
---

Design cache systems so that higher-level components control when cache entries are invalidated or cleaned up, rather than having cache operations happen automatically at lower levels. This allows callers to make informed decisions about cache lifecycle based on their broader context and requirements.

Lower-level components should provide cache management methods but not automatically invoke them. Instead, let the calling code decide the optimal timing for cache operations based on request boundaries, configuration changes, or other application-specific events.

Example of problematic automatic cleanup:
```rust
// Don't do this - automatic cleanup removes caller control
.map_err(JsErrorBox::from_err)?;
self.parsed_source_cache.free(&specifier); // Automatic cleanup
```

Better approach - let caller control:
```rust
// Provide cleanup methods but let caller decide when to use them
impl CachedProvider {
    pub fn clear_cache(&self) { /* cleanup logic */ }
}

// Caller decides optimal timing (e.g., after request completion)
provider.process_request()?;
provider.clear_cache(); // Controlled by caller
```

This separation of concerns allows for more flexible caching strategies, such as keeping long-lived services with short-lived caches, and enables smarter invalidation timing that considers the broader application context.