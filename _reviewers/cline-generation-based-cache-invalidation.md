---
title: Generation-Based Cache Invalidation
description: 'When caching async results, ensure stale responses can’t overwrite fresh
  data, and only refetch when the cached value’s lifecycle actually changes.


  **Rules**'
repository: ClInE/cLiNe
label: Caching
language: TSX
comments_count: 2
repository_stars: 70838
---

When caching async results, ensure stale responses can’t overwrite fresh data, and only refetch when the cached value’s lifecycle actually changes.

**Rules**
1. **Version your cache entries (generation/token).** Store a monotonically increasing “generation” per cache key (e.g., file path). Increment it whenever you invalidate/drop the cached content.
2. **Discard superseded responses.** When an async response returns, apply it only if it matches the latest generation for that key.
3. **Retry only for initial failure (lifecycle-aware).** For values that are stable for the app’s lifetime (e.g., configuration resolved once), fetch once at startup; subsequent “refresh”/reconnect events should *not* trigger a reload after success—only retry if the initial lookup failed.
4. **Test stale-response races.** Add a test that keeps a read in-flight across an invalidation/refresh and verifies the stale response cannot replace the updated contents.

**Pattern (simplified)**
```ts
const generations = new Map<string, number>();
const cache = new Map<string, { data: string; generation: number }>();

function invalidate(key: string) {
  generations.set(key, (generations.get(key) ?? 0) + 1);
  cache.delete(key);
}

async function read(key: string, fetcher: () => Promise<string>) {
  const gen = generations.get(key) ?? 0;
  const data = await fetcher();

  // Apply only if still current
  if ((generations.get(key) ?? 0) !== gen) return;
  cache.set(key, { data, generation: gen });
  return data;
}
```

If you follow this, you prevent cache-related race conditions (stale async results winning) and avoid unnecessary reloads that waste work or reintroduce inconsistencies.