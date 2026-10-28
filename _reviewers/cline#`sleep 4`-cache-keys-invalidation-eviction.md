---
title: Cache keys, invalidation, eviction
description: When caching derived or remote data, make sure the cache key encodes
  every input that can change the correct answer (account scope, workspace root, plugin/registry
  state, execution mode, etc.). A cache keyed only on a file fingerprint or a single
  id will silently serve a stale or wrong value once an unkeyed input (sign-in state,
  feature-flag poll...
repository: cline/cline#`sleep 4`
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70979
---

When caching derived or remote data, make sure the cache key encodes every input that can change the correct answer (account scope, workspace root, plugin/registry state, execution mode, etc.). A cache keyed only on a file fingerprint or a single id will silently serve a stale or wrong value once an unkeyed input (sign-in state, feature-flag poll generation, plugin enabled/disabled status) changes underneath it. Only cache a result once the computation has cleanly succeeded — a failed load should not be cached as if it were final, since the next attempt may succeed without any input changing.

Prefer TTL-based, stale-while-revalidate reads for anything backed by a remote source: return the cached value immediately (no UI flicker) while kicking off a background refresh once the entry is older than its TTL, and let the normal "new data arrived" path (e.g., postState) propagate the refreshed value. Back off repeated failures with their own short retry window instead of hammering the source on every read. When a user makes an explicit choice (a button, a refresh action), bypass the cache rather than waiting for TTL expiry.

Finally, treat cache entries as owning resources, not just bytes: give every cache an explicit eviction/disposal policy (size budget, idle-iteration timeout, or membership-based pruning) and make sure eviction actually releases what it should (close connections, delete temp files, disassociate correctly-typed payloads) — e.g. a byte-budget cache must correctly account for all payload shapes (don't miss alternate field names like `mimeType` vs `mediaType` when computing size), and disk-backed caches need a dispose path so they don't grow unbounded across the process lifetime. Avoid recomputing or rewriting a cached artifact on every subsequent read; compute once, store the result, and only recompute when an invalidating input actually changes.

Example pattern for a TTL cache with background refresh and failure backoff:
```ts
class Lookup<T> {
  private value: T | undefined
  private failedAt: number | undefined
  private pending: Promise<void> | undefined

  read(key: string, load: () => Promise<T>): T | undefined {
    this.start(key, load) // kicks off background refresh if stale/expired
    return this.value // never blocks; may be stale momentarily
  }
}
```