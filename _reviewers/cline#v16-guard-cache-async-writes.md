---
title: Guard Cache Async Writes
description: When caching async data, ensure stale in-flight responses can’t overwrite
  newer cache state, and invalidate only when the underlying lifetime actually changes.
repository: cline/cline#v16
label: Caching
language: TSX
comments_count: 3
repository_stars: 70882
---

When caching async data, ensure stale in-flight responses can’t overwrite newer cache state, and invalidate only when the underlying lifetime actually changes.

Apply these rules:
1) Version your cache entries
- Maintain a per-key “generation” (or request id/version).
- Increment/bump generation whenever you drop/refresh that key.
- When an async read completes, write to cache only if its generation still matches.

2) Coordinate invalidation with in-flight reads
- If data is already loading when a new snapshot arrives, don’t cancel/clear blindly.
- Mark it stale if needed, but allow the in-flight response to land; then schedule at most one follow-up read to reconcile.

3) Invalidate with correct scope/lifetime
- Don’t reload stable configuration on unrelated refreshes.
- Resolve once at startup for app-lifetime constants; reconnect should only retry if the initial lookup failed.

Example pattern (generation-guarded cache writes):
```ts
const generation = new Map<string, number>();

function invalidate(keys: Iterable<string>) {
  for (const k of keys) generation.set(k, (generation.get(k) ?? 0) + 1);
}

async function readAndCache(key: string) {
  const gen = generation.get(key) ?? 0; // capture
  const data = await fetchSomething(key); // async

  // only apply if still current
  if ((generation.get(key) ?? 0) !== gen) return;
  cache.set(key, data);
}
```
Add a test that holds a read in-flight, triggers refresh/invalidation, and asserts the late response does not replace the fresh cache state.