---
title: Cache Key Consistency
description: 'When you cache UI/model state, make the cache key and lifecycle unambiguous:


  - **Key boundary:** Perform the cache lookup using the exact key form the cache
  was populated with. Apply normalization/transformation *after* the lookup (only
  when constructing the output key/label), unless you also normalize consistently
  when inserting.'
repository: warpdotdev/warp
label: Caching
language: Rust
comments_count: 4
repository_stars: 56893
---

When you cache UI/model state, make the cache key and lifecycle unambiguous:

- **Key boundary:** Perform the cache lookup using the exact key form the cache was populated with. Apply normalization/transformation *after* the lookup (only when constructing the output key/label), unless you also normalize consistently when inserting.
- **Persisted entries:** If a cache/state entry must survive across renders, **insert and retain** a persistent handle/entry on first use. Avoid “transient defaults” that get re-created each render frame.
- **Granular keys:** Use the most granular stable identifier available (e.g., per-message/per-conversation id) so state doesn’t collide.
- **Refresh/invalidation:** Keep refresh logic reachable when upstream data may change externally, and remove cached entries when the underlying entity is deleted.

Example (pattern):
```rust
// 1) Cache lookup should use the cache’s expected raw key.
let candidate = pathbuf; // raw
if let Some(hit) = detected_repos_cache.get(&candidate) {
    // 2) Normalize only when constructing the stable group key/label.
    let group_key = ProjectGroupKey::Root(normalize_project_group_path(hit.path.clone()));
    return group_key;
}

// 3) Persist per-entity state; don’t use a transient default.
self.mouse_states
    .entry(conversation_id)
    .or_default(); // ensures the handle exists and is reused

// 4) Remove on deletion.
self.mouse_states.remove(&conversation_id);
```

Apply this checklist anytime you see `HashMap`-backed state, memoized computations, or “lookup + derived key” flows—most cache bugs here come from key normalization order, missing persistence, or missing refresh/invalidation paths.