---
title: Cache Eviction And Reset
description: 'In-memory caches must have a bounded lifecycle and must be keyed in
  a stable, minimal way. Avoid using entire mutable store objects as cache keys, especially
  for values derived from frequently changing inputs (e.g., keystrokes). Also, treat
  “force reset” actions as cache invalidation: clear any client state (and dependent
  cached computations) that would...'
repository: facebook/react#b15
label: Caching
language: TSX
comments_count: 2
repository_stars: 251891
---

In-memory caches must have a bounded lifecycle and must be keyed in a stable, minimal way. Avoid using entire mutable store objects as cache keys, especially for values derived from frequently changing inputs (e.g., keystrokes). Also, treat “force reset” actions as cache invalidation: clear any client state (and dependent cached computations) that would change derived outputs.

Apply this standard:
- Use a stable, minimal cache key (only the fields that affect the computation/result), not the whole store object.
- Add eviction (e.g., LRU) and/or TTL for Promise/result caches to prevent unbounded growth.
- On full/force reset, clear relevant cache entries and state so stale derived results aren’t reused.

Example (bounded cache + stable key):
```ts
// Stable key: only inputs that affect tabify
function makeTabifyKey(source: string, compilerOutput: CompilerOutput, showInternals: boolean) {
  return JSON.stringify({ source, showInternals, /* include any compilerOutput fields that affect output */ });
}

const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({
  max: 200,           // tune
  ttlMs: 30_000,      // tune
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = makeTabifyKey(store.source, compilerOutput, store.showInternals);
  const cached = tabifyCache.get(key);
  if (cached) return cached;

  const p = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  tabifyCache.set(key, p);
  return p;
}

// On force reset
function forceReset() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore /* no state preservation */ } });
}
```