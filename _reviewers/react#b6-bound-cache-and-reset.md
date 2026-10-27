---
title: Bound Cache and Reset
description: 'When caching results in memory, ensure (1) the cache can’t grow unboundedly
  and (2) reset operations fully invalidate cached/client state.


  Apply this as:'
repository: facebook/react#b6
label: Caching
language: TSX
comments_count: 2
repository_stars: 251888
---

When caching results in memory, ensure (1) the cache can’t grow unboundedly and (2) reset operations fully invalidate cached/client state.

Apply this as:
- Key design: Use a stable, minimal, serializable key derived only from inputs that affect the cached computation (avoid using whole mutable objects as keys).
- Eviction/TTL: Use a bounded strategy (e.g., LRU) or TTL so entries/promises are cleaned up.
- Force reset invalidation: If the user action is a “force reset,” clear all relevant client state and cached data; do not preserve flags that affect computation/output unless explicitly intended.

Example (bounded LRU-style caching):
```ts
// Example shape: cache holds promises/results; eviction prevents growth on keystrokes.
const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({
  max: 100,
  // or configure TTL if appropriate
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = JSON.stringify({
    // include only fields that actually affect tabify()
    source: store.source,
    showInternals: store.showInternals,
    // include any other relevant inputs (avoid whole `store` object)
  });

  const existing = tabifyCache.get(key);
  if (existing) return existing;

  const result = tabify(store.source, compilerOutput, store.showInternals);
  tabifyCache.set(key, result);
  return result;
}

// On force reset: clear cache/state entirely (including showInternals if it affects behavior)
function forceReset() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore } });
}
```