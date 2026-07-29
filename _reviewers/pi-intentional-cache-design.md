---
title: Intentional Cache Design
description: 'Cache behavior should be justified by real reuse and measured impact.


  Apply this standard:

  1) Scope the cache correctly: for per-process/per-session data, prefer in-memory
  caching and avoid disk persistence unless it measurably reduces recomputation time
  on restart/resume.'
repository: earendil-works/pi
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 79783
---

Cache behavior should be justified by real reuse and measured impact.

Apply this standard:
1) Scope the cache correctly: for per-process/per-session data, prefer in-memory caching and avoid disk persistence unless it measurably reduces recomputation time on restart/resume.
2) Make eviction policy explicit: if you use a bounded Map/Set, document whether eviction is FIFO, LRU, etc., and why that policy fits the observed access pattern.
3) Size caches based on evidence: verify whether the cache is actually populated and whether larger sizes improve hit rate/latency; don’t pick sizes “because it seems fine.”
4) Define acceptable cold-start behavior: if cache misses on resume are minor and the system already recomputes shortly, it’s fine to start empty.

Example pattern (in-memory, bounded, explicit FIFO):
```ts
const CACHE_LIMIT = 512;
const cache = new Map<string, number>();

function getOrCompute(key: string, compute: () => number) {
  const v = cache.get(key);
  if (v !== undefined) return v;

  const next = compute();
  if (cache.size >= CACHE_LIMIT) {
    const firstKey = cache.keys().next().value; // FIFO eviction
    if (firstKey !== undefined) cache.delete(firstKey);
  }
  cache.set(key, next);
  return next;
}
```
If you need different behavior (e.g., true LRU), use an LRU structure or maintain recency explicitly—don’t assume insertion-order eviction matches your intent.