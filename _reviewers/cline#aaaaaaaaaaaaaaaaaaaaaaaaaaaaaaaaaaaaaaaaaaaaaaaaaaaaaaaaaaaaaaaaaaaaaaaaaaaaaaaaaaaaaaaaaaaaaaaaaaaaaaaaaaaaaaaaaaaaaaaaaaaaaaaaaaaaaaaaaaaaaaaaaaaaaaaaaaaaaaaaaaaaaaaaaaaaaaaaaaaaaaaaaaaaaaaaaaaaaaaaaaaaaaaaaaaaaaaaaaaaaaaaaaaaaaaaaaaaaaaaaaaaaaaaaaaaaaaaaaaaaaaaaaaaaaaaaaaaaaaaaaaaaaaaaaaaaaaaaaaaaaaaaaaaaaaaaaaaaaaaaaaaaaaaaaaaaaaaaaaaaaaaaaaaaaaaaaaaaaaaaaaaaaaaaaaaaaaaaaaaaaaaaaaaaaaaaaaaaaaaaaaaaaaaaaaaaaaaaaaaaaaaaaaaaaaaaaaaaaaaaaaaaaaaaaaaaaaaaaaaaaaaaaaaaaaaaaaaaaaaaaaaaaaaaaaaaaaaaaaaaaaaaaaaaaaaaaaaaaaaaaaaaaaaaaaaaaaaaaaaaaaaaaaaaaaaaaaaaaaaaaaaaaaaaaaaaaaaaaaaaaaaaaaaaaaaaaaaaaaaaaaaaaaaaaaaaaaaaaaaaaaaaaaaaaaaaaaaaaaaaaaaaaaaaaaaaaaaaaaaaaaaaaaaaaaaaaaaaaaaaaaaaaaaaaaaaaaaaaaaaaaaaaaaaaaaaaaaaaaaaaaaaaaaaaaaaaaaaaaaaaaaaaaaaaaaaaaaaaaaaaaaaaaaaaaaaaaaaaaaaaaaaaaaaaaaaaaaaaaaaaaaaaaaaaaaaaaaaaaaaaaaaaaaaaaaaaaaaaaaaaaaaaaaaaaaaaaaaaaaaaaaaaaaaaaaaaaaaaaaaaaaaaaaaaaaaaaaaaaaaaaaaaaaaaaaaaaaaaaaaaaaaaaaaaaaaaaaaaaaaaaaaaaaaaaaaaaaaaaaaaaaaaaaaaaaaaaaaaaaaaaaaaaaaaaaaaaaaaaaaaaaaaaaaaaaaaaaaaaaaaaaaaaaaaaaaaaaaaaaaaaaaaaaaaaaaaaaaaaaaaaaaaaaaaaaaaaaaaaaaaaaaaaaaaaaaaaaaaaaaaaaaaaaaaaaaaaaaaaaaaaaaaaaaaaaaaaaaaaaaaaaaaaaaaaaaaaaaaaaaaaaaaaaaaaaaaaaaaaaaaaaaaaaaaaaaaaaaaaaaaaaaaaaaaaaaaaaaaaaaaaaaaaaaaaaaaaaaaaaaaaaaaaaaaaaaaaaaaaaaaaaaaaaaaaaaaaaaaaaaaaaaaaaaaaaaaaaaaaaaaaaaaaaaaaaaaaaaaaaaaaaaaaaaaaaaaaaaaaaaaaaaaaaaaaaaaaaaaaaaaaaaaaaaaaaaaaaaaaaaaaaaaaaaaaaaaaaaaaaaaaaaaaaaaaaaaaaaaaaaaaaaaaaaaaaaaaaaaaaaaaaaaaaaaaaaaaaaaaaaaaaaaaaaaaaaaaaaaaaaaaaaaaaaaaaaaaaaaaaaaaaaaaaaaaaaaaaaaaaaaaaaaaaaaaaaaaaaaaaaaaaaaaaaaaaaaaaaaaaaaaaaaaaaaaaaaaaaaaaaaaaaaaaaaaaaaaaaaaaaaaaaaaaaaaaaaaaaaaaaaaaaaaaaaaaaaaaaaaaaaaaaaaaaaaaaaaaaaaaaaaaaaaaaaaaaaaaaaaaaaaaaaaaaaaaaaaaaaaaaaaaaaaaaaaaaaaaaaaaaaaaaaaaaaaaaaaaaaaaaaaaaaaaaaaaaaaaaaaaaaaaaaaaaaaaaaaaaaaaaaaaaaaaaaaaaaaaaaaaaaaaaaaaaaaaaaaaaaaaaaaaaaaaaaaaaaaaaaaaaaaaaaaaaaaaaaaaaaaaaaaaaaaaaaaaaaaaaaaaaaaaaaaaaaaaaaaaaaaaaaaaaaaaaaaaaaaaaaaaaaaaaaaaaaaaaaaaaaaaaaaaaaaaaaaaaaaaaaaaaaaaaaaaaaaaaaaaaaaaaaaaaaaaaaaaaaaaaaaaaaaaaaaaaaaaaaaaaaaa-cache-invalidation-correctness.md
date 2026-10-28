---
title: Cache invalidation correctness
description: A cached value is only as trustworthy as the mechanism that decides when
  to stop trusting it. Across several reviews, caches went stale or returned wrong
  data because the key didn't capture everything the value depended on, or because
  nothing explicitly invalidated the cache when its underlying source changed.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70968
---

A cached value is only as trustworthy as the mechanism that decides when to stop trusting it. Across several reviews, caches went stale or returned wrong data because the key didn't capture everything the value depended on, or because nothing explicitly invalidated the cache when its underlying source changed.

Apply these rules whenever adding or touching a cache:

1. **Key on every input that affects the result.** If a cached computation depends on a setting, a registry/enabled state, an execution mode, or a tool's arguments, that value must be part of the cache key (or checked at read time), not just the "obvious" identifier. A plugin-tools cache keyed only on file paths missed a plugin being toggled off; a pinned-read cache now keys on tool *and* arguments so an edited pin doesn't serve the old result.

2. **Don't trust a live connection or elapsed time alone as proof of freshness.** A retained socket/host is not evidence the cached status is still current — revalidate the cached value against the authoritative record on every use (e.g., re-check a remembered "settled" status against the record's `updatedAt`), the same check applied on restart.

3. **Invalidate explicitly when a dependency changes**, rather than waiting for a TTL to expire. Toggling a feature flag that changes what a cache should return must call `invalidateCache()` before state is re-read; editing a cached pin should bump a revision so the next refresh picks it up immediately instead of after the full TTL.

4. **Never let a failed population attempt leave the cache believing it's "warm" or "in flight" forever.** If a fetch fails to produce a usable value, clear the pending/attempted marker so the next read retries, and only propagate/post the refreshed state when the cache was actually filled.

5. **For TTL-based caches serving UI, prefer stale-while-revalidate**: return the last known value immediately (avoid flicker) while refreshing in the background, and provide an explicit force-refresh path for the user-triggered case.

6. **Key warm-up/pre-fetch operations on the same identity the consumer will use later**, not on an incidental value (e.g., process cwd) that may differ from the resolved workspace/account/session key — a warm-up that targets the wrong key never helps the real cache lookup.

Example pattern for a revalidated entry:
```ts
function upsertRecord(record: Record): Entry {
  const existing = entries.get(record.id);
  if (existing) {
    existing.record = record;
    // A retained connection is not proof of continuous observation;
    // revalidate the settled value against the new record version.
    if (existing.cachedStatus && isSettled(existing.cachedStatus)) {
      existing.cachedStatus = rememberedStatusOf(record);
    }
    return existing;
  }
  ...
}
```