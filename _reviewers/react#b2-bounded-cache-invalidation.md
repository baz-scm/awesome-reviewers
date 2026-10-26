---
title: Bounded Cache Invalidation
description: 'When caching computed results, ensure the cache is bounded and that
  “force reset” paths fully invalidate any cached/derived state.


  - Use stable, minimal cache keys (derive from the specific inputs that change).
  Avoid using whole mutable objects (e.g., a full `store`) as `Map` keys.'
repository: facebook/react#b2
label: Caching
language: TSX
comments_count: 2
repository_stars: 251882
---

When caching computed results, ensure the cache is bounded and that “force reset” paths fully invalidate any cached/derived state.

- Use stable, minimal cache keys (derive from the specific inputs that change). Avoid using whole mutable objects (e.g., a full `store`) as `Map` keys.
- Bound cache growth with an LRU (and/or TTL). Evict old entries so caches don’t grow on frequent events like keystrokes.
- On a true reset, clear cached entries and reset all relevant flags that affect computation—don’t selectively preserve values like `showInternals` if the intent is “entirely clear client state.”

Example (bounded LRU + minimal key):
```ts
// Keep a bounded cache (size limit) and clear it on force reset.
const LRU_LIMIT = 100;
const tabifyCache = new Map<string, Promise<Map<string, ReactNode>>>();

function cacheGet(key: string) {
  const hit = tabifyCache.get(key);
  if (!hit) return undefined;
  // LRU bump
  tabifyCache.delete(key);
  tabifyCache.set(key, hit);
  return hit;
}

function cacheSet(key: string, value: Promise<Map<string, ReactNode>>) {
  if (tabifyCache.has(key)) tabifyCache.delete(key);
  tabifyCache.set(key, value);
  if (tabifyCache.size > LRU_LIMIT) {
    const firstKey = tabifyCache.keys().next().value;
    tabifyCache.delete(firstKey);
  }
}

function cacheClear() {
  tabifyCache.clear();
}

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = JSON.stringify({
    source: store.source,
    showInternals: store.showInternals,
    // include only other primitive inputs that affect tabify
  });

  const cached = cacheGet(key);
  if (cached) return cached;

  const result = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  cacheSet(key, result);
  return result;
}

// On force reset:
// cacheClear(); dispatchStore({ type: 'setStore', payload: { store: defaultStore } });
```
