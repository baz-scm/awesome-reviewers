---
title: Versioned cache invalidation
description: 'When caching async data per key, ensure cache invalidation is *safe
  under concurrency* and that you only refetch on real dependency changes.


  1) Prevent stale overwrites (generation/request-id pattern)'
repository: cline/cline#v9
label: Caching
language: TSX
comments_count: 2
repository_stars: 70868
---

When caching async data per key, ensure cache invalidation is *safe under concurrency* and that you only refetch on real dependency changes.

1) Prevent stale overwrites (generation/request-id pattern)
- For each cached key (e.g., file path), keep a monotonically increasing “generation” (or request id).
- When you drop/invalidate the cache (refresh, close tab, external edit), bump the generation.
- When an async response arrives, apply it only if it matches the latest generation for that key; otherwise discard it.
- Add a regression test that keeps an in-flight read across a refresh and asserts stale responses cannot replace fresh data.

2) Don’t refetch stable values on unrelated refreshes
- If a value/config is fixed for the app/environment lifetime, resolve it once (typically at startup or the first successful lookup) and reuse it.
- Reconnect should retry only the initial lookup if it failed; after success, don’t reload it on every account refresh.

Example (generation-based per-path cache)
```ts
const genByPath = new Map<string, number>();
const [cacheByPath, setCacheByPath] = useState(new Map<string, string>());

async function readPath(path: string) {
  const gen = (genByPath.get(path) ?? 0);

  const result = await fetchFromServer(path);

  // Apply only if still current
  if ((genByPath.get(path) ?? 0) !== gen) return;
  setCacheByPath((m) => new Map(m).set(path, result));
}

function invalidatePath(path: string) {
  genByPath.set(path, (genByPath.get(path) ?? 0) + 1);
  setCacheByPath((m) => {
    const next = new Map(m);
    next.delete(path);
    return next;
  });
}
```
This standard eliminates a common caching failure mode (stale async results overwriting freshly invalidated state) and reduces unnecessary reloads for lifecycle-stable data.