---
title: Cache keys and freshness
description: 'Design every cache around two explicit decisions: what belongs in the
  key, and how staleness is handled.


  1. The cache key must include every input that can change the correctness of the
  cached value — not just the obvious identity. A plugin-tools cache that keyed only
  on file contents served stale results after a plugin was toggled off/on; the fix
  added...'
repository: "cline/cline\t"
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 70947
---

Design every cache around two explicit decisions: what belongs in the key, and how staleness is handled.

1. The cache key must include every input that can change the correctness of the cached value — not just the obvious identity. A plugin-tools cache that keyed only on file contents served stale results after a plugin was toggled off/on; the fix added registry state and execution mode to the key. A warm-up cache keyed by process cwd warmed the wrong entry once the real lookup key (the resolved workspace path) diverged from it. Before caching, enumerate every value the caller reads to resolve the result and fold it into the key (or invalidate explicitly when it changes).

2. Prefer a bounded freshness window with background refresh (stale-while-revalidate) over either "cache forever" or "always blocking fetch". Serve the last known value immediately, kick off a refresh once the entry is older than `maxAgeMs`, and let the next read/refresh pick up the new value with no UI flicker:

```ts
class Lookup<T> {
  private value?: T
  private loadedAt?: number
  read(key: string, load: () => Promise<T>): T | undefined {
    this.start(key, load, /*refresh*/ false)
    return this.value // stale-but-served while a refresh may be in flight
  }
  private aged(): boolean {
    return this.maxAgeMs !== undefined &&
      this.loadedAt !== undefined &&
      this.now() - this.loadedAt >= this.maxAgeMs
  }
}
```
Pick the TTL deliberately per input (e.g. 60s for data only another surface can change, 10s for local/workspace state) rather than reusing one global value.

3. A failed fetch must not permanently poison the cache slot. Release the "pending" state on failure so the next read retries (optionally after a short backoff), instead of leaving a dead warm-up handle or an empty cache that never refills. Only persist successful/clean results; a run that failed should stay re-triable rather than being cached as the answer.

4. Accept that distributed/externally-mutable caches (e.g. access changing in a browser tab) can only be narrowed, not closed — document the acceptable staleness window instead of overengineering perfect consistency.