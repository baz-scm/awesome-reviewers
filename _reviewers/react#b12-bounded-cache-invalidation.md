---
title: Bounded cache invalidation
description: 'When caching derived results, ensure the cache is **bounded** and that
  entries are invalidated on **force reset**.


  Apply two rules:

  1) **Key caches by stable, minimal identifiers—not whole objects.** High-cardinality
  keys (e.g., per-keystroke mutable store objects) will cause unbounded growth.'
repository: facebook/react#b12
label: Caching
language: TSX
comments_count: 2
repository_stars: 251896
---

When caching derived results, ensure the cache is **bounded** and that entries are invalidated on **force reset**.

Apply two rules:
1) **Key caches by stable, minimal identifiers—not whole objects.** High-cardinality keys (e.g., per-keystroke mutable store objects) will cause unbounded growth.
2) **Use bounded eviction (LRU/TTL) and clear cache/state on reset.** A “force reset” should fully invalidate cached derived output and restore defaults (including flags) so stale UI does not persist.

Example (bounded, stable-key caching + reset invalidation):
```ts
// Bounded LRU-style cache (pseudo-implementation)
const tabifyCache = new LruMap<string, Promise<Map<string, ReactNode>>>(100);

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  // Use a stable minimal key; do NOT use the whole `store` object.
  const cacheKey = JSON.stringify({
    source: store.source,
    showInternals: store.showInternals,
    // include any other fields that affect output
    // e.g., compilerOutput.version
  });

  const existing = tabifyCache.get(cacheKey);
  if (existing) return existing;

  const result = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  tabifyCache.set(cacheKey, result);
  return result;
}

// On force reset: clear client state AND derived caches.
function forceReset() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore /* defaults incl. showInternals */ } });
}
```