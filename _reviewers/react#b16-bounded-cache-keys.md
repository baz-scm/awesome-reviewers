---
title: Bounded Cache Keys
description: When caching derived/async results, ensure the cache cannot grow unbounded
  and is correctly invalidated on resets. Avoid using large, mutable objects (like
  the entire `store`) as cache keys—this can create a new key per keystroke and retain
  promises forever. Use stable, minimal keys and a bounded eviction strategy (LRU
  or TTL), and make “force reset” paths...
repository: facebook/react#b16
label: Caching
language: TSX
comments_count: 2
repository_stars: 251891
---

When caching derived/async results, ensure the cache cannot grow unbounded and is correctly invalidated on resets. Avoid using large, mutable objects (like the entire `store`) as cache keys—this can create a new key per keystroke and retain promises forever. Use stable, minimal keys and a bounded eviction strategy (LRU or TTL), and make “force reset” paths clear all cache/client-derived state associated with the previous session.

Example pattern:
```ts
// Use a stable key (e.g., source text + flags + compilation version), not the whole store object.
function cacheKey(store: Store): string {
  return [store.source.version, store.source.textHash, store.showInternals].join(':');
}

// Bounded LRU cache for promises/results.
import LRU from 'lru-cache';
const tabifyCache = new LRU<string, Promise<Map<string, ReactNode>>>({
  max: 100,
  ttl: 30_000,
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = cacheKey(store);
  const hit = tabifyCache.get(key);
  if (hit) return hit;

  const result = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  tabifyCache.set(key, result);
  return result;
}

// On force reset: clear any cached derived state tied to the previous store.
function forceResetPlayground() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore } });
}
```
Apply this anytime you cache derived UI data or async computations: choose stable keys, enforce eviction/TTL, and ensure reset/invalidation fully clears cached results rather than preserving stale flags/state.