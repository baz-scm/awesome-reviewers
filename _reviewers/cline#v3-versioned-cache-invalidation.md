---
title: Versioned Cache Invalidation
description: For cached async data, prevent stale in-flight responses from overwriting
  newer state, and refetch only when the underlying inputs can actually change.
repository: cline/cline#v3
label: Caching
language: TSX
comments_count: 2
repository_stars: 70863
---

For cached async data, prevent stale in-flight responses from overwriting newer state, and refetch only when the underlying inputs can actually change.

Apply two rules:
1) Version/token per cache key (generation)
- When you invalidate/drop a cache entry, bump a “generation” tied to that key.
- When an async response arrives, commit it only if it matches the latest generation; otherwise discard it.
- Add a test that keeps a read in-flight while triggering a refresh/invalidation, then asserts stale data cannot replace the fresh cache.

Example pattern:

```ts
const genByKey = new Map<string, number>();
const [cache, setCache] = useState(new Map<string, any>());

function bumpGen(key: string) {
  genByKey.set(key, (genByKey.get(key) ?? 0) + 1);
}

async function fetchAndCache(key: string) {
  const gen = genByKey.get(key) ?? 0;
  const result = await apiFetch(key);

  // Commit only if nothing invalidated this key since the request started.
  if ((genByKey.get(key) ?? 0) !== gen) return;
  setCache((current) => {
    const next = new Map(current);
    next.set(key, result);
    return next;
  });
}

function refreshKey(key: string) {
  bumpGen(key);      // invalidate
  void fetchAndCache(key); // fetch new
}
```

2) Fetch policy: load once when stable, refresh only when mutable
- If a value is determined by long-lived application configuration (e.g., tied to the app lifecycle) and cannot change during account refresh/reconnect, resolve it once at startup and reuse it.
- If the value depends on something that can change (backend/env/storage), invalidate and refetch at that specific boundary—not on unrelated “refresh” actions.

This avoids two common caching failures: (a) stale async overwrites after invalidation, and (b) wasted/incorrect re-fetching triggered by the wrong lifecycle event.