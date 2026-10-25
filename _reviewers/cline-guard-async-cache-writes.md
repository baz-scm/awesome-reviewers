---
title: Guard Async Cache Writes
description: 'When caching async data, ensure late/out-of-order responses can’t overwrite
  newer state.


  **Do this**

  - **Use per-key sequencing**: attach a monotonically increasing “generation” (or
  token) to each cache key when you start a read; bump/invalidate the generation whenever
  you drop that key’s cache (refresh, close tab, edit). When a response arrives, apply
  it...'
repository: CLINE/cline
label: Caching
language: TSX
comments_count: 4
repository_stars: 70839
---

When caching async data, ensure late/out-of-order responses can’t overwrite newer state.

**Do this**
- **Use per-key sequencing**: attach a monotonically increasing “generation” (or token) to each cache key when you start a read; bump/invalidate the generation whenever you drop that key’s cache (refresh, close tab, edit). When a response arrives, apply it **only if** its generation still matches.
- **Or use stale markers + controlled follow-up**: on invalidation (e.g., snapshot/root changes), mark cached entries as `stale` and update logic so in-flight reads don’t get clobbered; if a stale response arrives, keep it and then trigger **exactly one** follow-up read.
- **Centralize invalidation paths**: route manual refresh/updates through the same invalidation mechanism rather than clearing caches in a way that bypasses your ordering model.
- **Treat stable configuration as single-resolution**: if the underlying environment is fixed for the session, resolve it once at startup and don’t re-fetch it on unrelated “refresh” events.
- **Keep authority with current user intent**: avoid patterns where an async read/write can flip the UI selection after the user changed it; store user choices and only derive dependent data from the latest state.

**Example (generation guard)**
```ts
const readGen = new Map<string, number>();

function invalidate(keys: Iterable<string>) {
  for (const k of keys) readGen.set(k, (readGen.get(k) ?? 0) + 1);
}

async function readWithGuard<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const gen = readGen.get(key) ?? 0;
  const value = await fetcher();
  if ((readGen.get(key) ?? 0) !== gen) {
    // stale response: drop
    throw new Error("stale");
  }
  return value;
}
```

**Test requirement**
- Add a unit/integration test that holds an async read “in flight,” triggers invalidation/refresh, and asserts the late response does **not** replace the fresh cached content (and that any follow-up read behavior is deterministic).