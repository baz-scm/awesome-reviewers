---
title: Versioned Cache Invalidation
description: 'For any per-key cached async data, prevent stale responses from overwriting
  newer state by versioning reads and only committing the latest generation. Also,
  align cache refresh/fetch policies with dependency stability: fetch stable configuration
  once (or retry only if the initial fetch failed) instead of reloading it on unrelated
  refreshes.'
repository: cline/cline#v8
label: Caching
language: TSX
comments_count: 2
repository_stars: 70867
---

For any per-key cached async data, prevent stale responses from overwriting newer state by versioning reads and only committing the latest generation. Also, align cache refresh/fetch policies with dependency stability: fetch stable configuration once (or retry only if the initial fetch failed) instead of reloading it on unrelated refreshes.

Apply it like this:
- Version reads: maintain a monotonically increasing “generation” (or request id) per cache key.
- Invalidate by bumping generation: when you drop/refresh cache entries (e.g., tab close, refresh action, user edit), bump the generation for that key.
- Commit guard: when an async response returns, only apply it if it matches the current generation; otherwise discard it.
- Stable values: if the dependency is fixed for the app lifetime, resolve once at startup and don’t reload on every account refresh/reconnect.

Example (generation-guarded cached reads):

```ts
const generationByKey = new Map<string, number>();

function bumpGeneration(key: string) {
  const next = (generationByKey.get(key) ?? 0) + 1;
  generationByKey.set(key, next);
  return next;
}

async function fetchAndCache(key: string, read: () => Promise<string>, commit: (v: string) => void) {
  const genAtStart = bumpGeneration(key); // treat as a new read “version”
  const value = await read();

  // Only commit if no newer invalidation happened.
  if ((generationByKey.get(key) ?? 0) === genAtStart) {
    commit(value);
  }
}
```

Cache policy checklist:
- If invalidation can happen while a request is in-flight → use generation guarding.
- If the underlying dependency is stable across the lifecycle (e.g., environment/backend fixed) → fetch once; reconnect should only retry a failed initial lookup, not re-fetch on every refresh event.