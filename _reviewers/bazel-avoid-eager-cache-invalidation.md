---
title: Avoid eager cache invalidation
description: Resist the urge to eagerly invalidate cache entries unless you have definitive
  proof that the cached data is invalid and cannot provide value for future operations.
  Cache entries can still be valuable even when their associated remote artifacts
  have expired or been removed.
repository: bazelbuild/bazel
label: Caching
language: Java
comments_count: 3
repository_stars: 24489
---

Resist the urge to eagerly invalidate cache entries unless you have definitive proof that the cached data is invalid and cannot provide value for future operations. Cache entries can still be valuable even when their associated remote artifacts have expired or been removed.

The key principle is that cache invalidation should be conservative - err on the side of keeping potentially useful cache entries rather than aggressively removing them. Even when remote cache artifacts are no longer available, the local cache entry may still save build time for actions whose outputs are never materialized.

Consider these approaches instead of eager invalidation:
- Use lazy invalidation where cache entries are only removed when they're proven to cause issues
- Implement cache validation checks (like symlink detection) to determine if cached results are still valid
- Clean up only entries that are definitively stale (like server-lifetime entries from previous instances)

Example of conservative cache management:
```java
if (actionCache != null && token != null) {
  // Don't eagerly delete - cache entry can still save build time 
  // for actions whose outputs are never materialized
  if (token.dirty) {
    actionCache.put(token.key, token.entry);
  }
}

// Only clean up definitively stale entries
actionCache.removeIf(entry -> 
  entry.getOutputFiles().values().stream()
    .anyMatch(e -> e.getExpireAtEpochMilli() == SERVER_EXPIRATION_SENTINEL));
```

This approach maximizes cache hit rates while maintaining correctness, leading to better build performance overall.