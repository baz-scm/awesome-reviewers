---
title: Versioned Async Cache Reads
description: When caching data that is populated via async requests, guard against
  late/stale responses overwriting newer state. Use explicit versioning plus clear
  cache lifecycles.
repository: cline/cline#v20
label: Caching
language: TSX
comments_count: 3
repository_stars: 70886
---

When caching data that is populated via async requests, guard against late/stale responses overwriting newer state. Use explicit versioning plus clear cache lifecycles.

Rules:
1. Version every cache entry (or request) with a monotonic “generation” (per key, path, or selection). Increment/bump the generation whenever you invalidate/drop the cached entry (refresh, tab close, external edit, etc.).
2. When an async response returns, commit it only if its generation still matches the latest generation for that key. Otherwise, discard it.
3. Avoid reloading stable configuration on unrelated refreshes—load once at startup and keep it unless the underlying identity actually changes.
4. Separate cached reads from user-intent writes: async lookups should update derived state only when they correspond to the latest user selection; late lookups must not flip persisted intent.
5. Add regression tests for race conditions (e.g., hold a read open, trigger refresh/invalidation, verify stale response doesn’t replace fresh data).

Example pattern:
```ts
const generationByKey = new Map<string, number>();

function bumpGeneration(key: string) {
  generationByKey.set(key, (generationByKey.get(key) ?? 0) + 1);
  return generationByKey.get(key)!;
}

async function loadWithGuard(key: string) {
  const gen = bumpGeneration(key); // invalidate + capture latest
  const result = await fetchDataForKey(key);

  // Only apply if still current
  if ((generationByKey.get(key) ?? 0) !== gen) return;
  cache.set(key, result);
}
```

Apply this anywhere cached UI/data can be populated after a user action or refresh; it prevents the most common caching failure mode: stale async responses winning the race.