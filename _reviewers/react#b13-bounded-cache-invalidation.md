---
title: Bounded Cache Invalidation
description: 'When caching computed UI/data, ensure the cache has a clear lifecycle:
  (1) prevent unbounded growth by using bounded caches (e.g., LRU) or TTL, and (2)
  make “force reset” semantics actually invalidate/clear all relevant cached/client
  state.'
repository: facebook/react#b13
label: Caching
language: TSX
comments_count: 2
repository_stars: 251893
---

When caching computed UI/data, ensure the cache has a clear lifecycle: (1) prevent unbounded growth by using bounded caches (e.g., LRU) or TTL, and (2) make “force reset” semantics actually invalidate/clear all relevant cached/client state.

Key rules:
- Use small, stable cache keys (IDs/derived primitives), not whole mutable objects.
- Add eviction (LRU) and/or TTL so caches can’t grow forever (e.g., per-keystroke).
- On a full reset action, clear/replace state so cached derivations don’t accidentally preserve flags that should be reset.

Example (bounded cache + stable key):
```ts
// Pseudocode: bounded LRU/TTL cache
const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({
  max: 100, // tune
  ttlMs: 10_000,
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  // Derive a compact, stable key instead of using the whole store object
  const key = `${store.sourceVersion}:${store.showInternals ? 1 : 0}`;

  const cached = tabifyCache.get(key);
  if (cached) return cached;

  const result = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  tabifyCache.set(key, result);
  return result;
}
```
If the UI includes a “force reset” action, treat it as invalidation: don’t carry over options/flags (like `showInternals`) that should be cleared for a truly fresh client state.