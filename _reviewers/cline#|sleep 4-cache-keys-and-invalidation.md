---
title: Cache keys and invalidation
description: 'Design every cache around the complete set of inputs that determine
  the validity of its value, and invalidate it whenever any of those inputs change.

  '
repository: cline/cline#|sleep 4
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70979
---

Design every cache around the complete set of inputs that determine the validity of its value, and invalidate it whenever any of those inputs change.

1. Key by everything that affects correctness. If a value depends on account scope, workspace path, plugin/registry state, or execution mode, include all of those in the key — not just the obvious ones. A cache keyed only on "plugin path" served stale tool lists after a plugin was toggled off because `state` wasn't part of the key; a service cache keyed on the wrong workspace path warmed up a key the UI never read from. When in doubt, add the dimension to the key rather than relying on a side invalidation call.

2. Invalidate proactively on every mutation that affects cached data, not just on the read path. Toggling a feature flag that changes what a list includes must call the cache's invalidate hook before the next state/read, e.g. `controller.invalidateTaskHistoryCache()` right after flipping `cloudSessionsEnabled`.

3. Prefer stale-while-revalidate for latency-sensitive reads: return the cached value immediately and refresh in the background, rather than blocking or showing nothing.
```ts
read(key: string, load: () => Promise<T>): T | undefined {
  this.start(key, load, /* refresh */ false) // kicks off background load if stale/missing
  return this.value // serve what we have now
}
```
Give each cached input its own TTL tuned to how fast it can change (e.g., a short TTL for a locally-checked-out branch, a longer one for remote repo permissions), and back off retries after a failed load instead of hammering the source.

4. Only let a background refresh trigger downstream side effects (re-render, re-post state, notifications) when the refreshed value actually differs from what's cached — a refresh that falls back to the same value must not re-arm another refresh/post on its own, or you get a self-sustaining loop.

5. Cache only well-defined, reusable outcomes. Don't cache a failed/partial computation under the same key as a success (fix it or let it retry on next read), and make sure whatever budget/eviction logic a cache uses (e.g., LRU by byte size) measures the data it's actually storing — a format mismatch (e.g. missing a field like `mimeType` vs `mediaType`) can mis-account size and evict unrelated, still-valid entries.