---
title: Bound and Invalidate Cache
description: When implementing in-memory caching (including promise caches and UI-derived
  caches), ensure (1) keys are stable and minimal (not whole high-churn objects) and
  (2) the cache is bounded and invalidated on explicit reset.
repository: facebook/react#b11
label: Caching
language: TSX
comments_count: 2
repository_stars: 251894
---

When implementing in-memory caching (including promise caches and UI-derived caches), ensure (1) keys are stable and minimal (not whole high-churn objects) and (2) the cache is bounded and invalidated on explicit reset.

Apply this by:
- Avoid using the entire `store` object (or other mutable/high-frequency state) as a cache key; instead derive a small, stable key from the specific inputs that affect the result.
- Use an eviction strategy (LRU) and/or TTL so the cache can’t grow unboundedly (e.g., on every keystroke).
- On a “force reset”/playground reset, clear any derived/cached state so stale render output can’t persist.

Example pattern:

```ts
// Use a stable key derived from inputs; avoid storing whole store objects.
function makeTabifyKey(source: string, showInternals: boolean): string {
  return `${showInternals ? 'internals' : 'public'}:${source}`;
}

// Use a bounded cache (LRU) to prevent unbounded growth.
const tabifyCache = new LRUMap<string, Promise<Map<string, ReactNode>>>({
  max: 100, // tune
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = makeTabifyKey(store.source, store.showInternals);
  const hit = tabifyCache.get(key);
  if (hit) return hit;

  const result = tabify(store.source, compilerOutput, store.showInternals);
  tabifyCache.set(key, result);
  return result;
}

// On force reset, clear cached/derived state.
function forceResetPlayground() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore } });
}
```

This prevents memory leaks/unbounded cache growth and ensures reset actions fully invalidate cached UI/client state.