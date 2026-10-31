---
title: Cache invalidation completeness
description: 'A cache is only as correct as the signals it watches. Before adding
  a cache, enumerate every input that can change the correct answer, and make sure
  each one either (a) is part of the cache key/fingerprint, (b) triggers an explicit
  invalidation call, or (c) is bounded by a TTL with background refresh. Problems
  seen repeatedly: a settings toggle changed what...'
repository: cline/cline?foo=bar
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 71082
---

A cache is only as correct as the signals it watches. Before adding a cache, enumerate every input that can change the correct answer, and make sure each one either (a) is part of the cache key/fingerprint, (b) triggers an explicit invalidation call, or (c) is bounded by a TTL with background refresh. Problems seen repeatedly: a settings toggle changed what a listing should contain but nothing invalidated the cache (fix: call `invalidateCache()` when the setting changes); a cache key omitted a dimension (plugin enabled/disabled state) that affects the result, so a disabled plugin kept being served from a stale entry (fix: fold state/`updatedAt`/execution mode into the cache key); a remembered value was treated as proof of continuous observation instead of being revalidated against the latest version of the underlying record (fix: always compare against the newest record, even for cache hits); and a byte-budget eviction policy miscounted certain content types, corrupting LRU accounting and evicting the wrong entries.

Guidelines to apply:
- Treat "what changed?" as a checklist when designing a cache: external state changes, feature flags, record versions/`updatedAt`, and content-type variants must all be covered.
- Prefer stale-while-revalidate over indefinite caching: return the cached value immediately but kick off a background refresh once a TTL elapses, so staleness is bounded and UI never blocks on a network round trip. Still provide an explicit force-refresh path for user-initiated actions.
```ts
read(key: string, load: () => Promise<T>): T | undefined {
  if (this.key !== key || this.isExpired()) {
    this.start(key, load) // background reload; keep old value until it lands
  }
  return this.value // never blocks; may be stale but bounded by TTL
}
```
- When a cache's correctness depends on a mutable record, re-validate against the latest version on every read rather than trusting a cached "settled" status indefinitely.
- Any cache that writes to disk or holds unbounded in-memory state must have an explicit disposal/cleanup path and accurate size accounting for eviction; don't rewrite/re-truncate cached content on every subsequent read when a one-time write at completion is sufficient.
- Document, in code comments near the cache, exactly which inputs it is keyed/invalidated on, so future changes that add a new input are forced to also consider cache correctness.