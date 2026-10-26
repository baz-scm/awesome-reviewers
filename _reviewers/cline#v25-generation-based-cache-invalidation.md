---
title: Generation-Based Cache Invalidation
description: 'When caching async data, make cache lifetime explicit and prevent stale/in-flight
  responses from overwriting fresh state.


  **Rules**

  1. **Resolve once when the value’s lifetime is the app/account lifetime.** If a
  configuration (e.g., base URL) cannot legitimately change for the supported runtime
  flow, fetch it once at startup and reuse it; don’t re-fetch...'
repository: cline/cline#v25
label: Caching
language: TSX
comments_count: 2
repository_stars: 70891
---

When caching async data, make cache lifetime explicit and prevent stale/in-flight responses from overwriting fresh state.

**Rules**
1. **Resolve once when the value’s lifetime is the app/account lifetime.** If a configuration (e.g., base URL) cannot legitimately change for the supported runtime flow, fetch it once at startup and reuse it; don’t re-fetch during unrelated “refresh account” flows.
2. **For anything that can be invalidated (refresh, eviction, tab close, edits), use a per-key “generation” (or request token).** Increment/bump the generation when you drop/evict the cached entry. When an async response returns, only apply it if its generation matches the current one; otherwise discard it.
3. **Test the race.** Add a test that keeps an async read “open” across a refresh/eviction and verifies that the stale response does not replace the fresh contents.

**Example pattern (generation/token)**
```ts
type Entry<T> = { generation: number; value?: T };
const cache = new Map<string, Entry<any>>();

async function readWithInvalidation<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const currentGeneration = (cache.get(key)?.generation ?? 0);

  const value = await fetcher();

  // Apply only if still current
  const latestGeneration = cache.get(key)?.generation ?? 0;
  if (latestGeneration !== currentGeneration) {
    // stale response; discard
    throw new Error("stale response");
  }

  cache.set(key, { generation: latestGeneration, value });
  return value;
}

function invalidate(key: string) {
  const prevGen = cache.get(key)?.generation ?? 0;
  cache.set(key, { generation: prevGen + 1 });
}

// Usage:
// invalidate(path) when you drop cached contents; stale in-flight responses are ignored.
```

Applying this standard avoids both (a) unnecessary reloads for values that should be stable, and (b) correctness bugs where stale cached async results race and overwrite newer data.