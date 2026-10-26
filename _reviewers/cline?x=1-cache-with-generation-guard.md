---
title: Cache with Generation Guard
description: "When caching async data, make invalidation explicit and prevent out-of-order\
  \ responses from overwriting newer state. \n\n**Standard**\n1. **Define cache lifetime/invalidation\
  \ triggers**: Only re-fetch when the underlying dependency actually changes. If\
  \ a value is stable for the app lifetime, resolve it once (e.g., during startup/initial\
  \ lookup) and don’t..."
repository: cline/cline?x=1
label: Caching
language: TSX
comments_count: 2
repository_stars: 70861
---

When caching async data, make invalidation explicit and prevent out-of-order responses from overwriting newer state. 

**Standard**
1. **Define cache lifetime/invalidation triggers**: Only re-fetch when the underlying dependency actually changes. If a value is stable for the app lifetime, resolve it once (e.g., during startup/initial lookup) and don’t reload it on unrelated “refresh” flows.
2. **Use a generation/sequence token for in-flight reads**: For any cached entry that can be invalidated while a request is running (refresh, tab close, agent edit), increment a per-key generation when dropping/invalidating the cache. When the request resolves, apply the result only if its generation still matches.
3. **Test the race**: Add a test that keeps a read in-flight across a refresh/invalidation and asserts the stale response can’t replace the newer cached contents.

**Example (generation guard pattern)**
```ts
const generationByPath = new Map<string, number>();
const cacheByPath = new Map<string, { value: string; generation: number }>();

function invalidatePath(path: string) {
  generationByPath.set(path, (generationByPath.get(path) ?? 0) + 1);
  cacheByPath.delete(path);
}

async function readPath(path: string) {
  const gen = generationByPath.get(path) ?? 0; // snapshot

  const value = await fetchFromBackend(path); // async

  // Apply only if not invalidated since the request started
  if ((generationByPath.get(path) ?? 0) !== gen) return cacheByPath.get(path);

  cacheByPath.set(path, { value, generation: gen });
  return value;
}
```

Follow this rule to improve both **cache correctness** (no stale overwrites) and **cache efficiency** (no unnecessary re-fetches).