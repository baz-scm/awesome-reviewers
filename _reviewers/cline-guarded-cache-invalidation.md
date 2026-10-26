---
title: Guarded Cache Invalidation
description: 'When caching async data per key, make invalidation race-safe and avoid
  unnecessary reloads.


  **1) Invalidate with per-key generations (or version tokens)**'
repository: Cline/Cline
label: Caching
language: TSX
comments_count: 3
repository_stars: 70840
---

When caching async data per key, make invalidation race-safe and avoid unnecessary reloads.

**1) Invalidate with per-key generations (or version tokens)**
- Every cache entry read should capture the current generation/version for its key.
- When you drop/refresh/expire a cache entry, increment that key’s generation.
- If a response arrives with an older generation, discard it so stale data can’t overwrite fresh cache.

**2) Coalesce refreshes to prevent duplicate reads**
- If a read is already in-flight and the cache is marked stale due to a newer snapshot/trigger, keep the in-flight result (don’t cancel it), then schedule **at most one** follow-up read after it completes.

**3) Invalidate only when dependencies can actually change**
- Don’t reload “stable” configuration during unrelated refresh flows. If the environment/backend is fixed for the app lifetime, fetch once at startup and only retry if the initial lookup failed.

Example pattern (generation-guarded reads):
```ts
const generationRef = useRef(new Map<string, number>());

function bump(keys: Iterable<string>) {
  for (const key of keys) {
    generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
  }
}

async function readForKey(key: string) {
  const gen = generationRef.current.get(key) ?? 0;

  const value = await fetchSomethingForKey(key);

  // Discard stale responses
  if ((generationRef.current.get(key) ?? 0) !== gen) return;

  setCache(key, value);
}

function refreshCache(keys: Iterable<string>) {
  bump(keys);
  for (const key of keys) void readForKey(key);
}
```
Apply this approach to file contents, diff snapshots, and any other cached async data where late responses or StrictMode remounts can cause out-of-order updates.