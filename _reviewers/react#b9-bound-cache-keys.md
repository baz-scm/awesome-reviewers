---
title: Bound cache keys
description: 'When caching results in UI/compilers, ensure both (1) caches are bounded
  and (2) cache/state is correctly invalidated on resets.


  Apply these rules:

  1. **Don’t use whole store/state objects as cache keys** if they change frequently
  (e.g., on every keystroke). Use a **stable, minimal key** derived from the specific
  inputs that affect the computed result.'
repository: facebook/react#b9
label: Caching
language: TSX
comments_count: 2
repository_stars: 251891
---

When caching results in UI/compilers, ensure both (1) caches are bounded and (2) cache/state is correctly invalidated on resets.

Apply these rules:
1. **Don’t use whole store/state objects as cache keys** if they change frequently (e.g., on every keystroke). Use a **stable, minimal key** derived from the specific inputs that affect the computed result.
2. **Prevent unbounded growth**: use a bounded cache (e.g., **LRU**) or enforce a **TTL** so old entries are evicted.
3. **On “force reset”**, clear/restore state in a way that **invalidates cached results** and does not preserve fields that should be reset (e.g., avoid carrying over UI/client flags that are meant to be cleared).

Example pattern (bounded + minimal key):
```ts
// Use derived inputs instead of the entire `store` object.
function cacheKey(store: Store, showInternals: boolean) {
  return JSON.stringify({
    source: store.source,
    showInternals,
  });
}

// Simple bounded Map (eviction can be LRU if you maintain access order).
const tabifyCache = new Map<string, Promise<Map<string, ReactNode>>>();
const MAX_ENTRIES = 200;

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = cacheKey(store, store.showInternals);

  const hit = tabifyCache.get(key);
  if (hit) return hit;

  // Evict when full (LRU would evict least-recently-used; this is placeholder eviction).
  if (tabifyCache.size >= MAX_ENTRIES) {
    const firstKey = tabifyCache.keys().next().value;
    tabifyCache.delete(firstKey);
  }

  const result = tabify(store.source, compilerOutput, store.showInternals);
  tabifyCache.set(key, result);
  return result;
}
```
And on a force reset, ensure you don’t retain reset-sensitive client fields/state that should be cleared, and invalidate any related cached computations accordingly.