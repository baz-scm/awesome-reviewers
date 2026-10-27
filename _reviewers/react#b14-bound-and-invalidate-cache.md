---
title: Bound and Invalidate Cache
description: 'Caches must not grow without limit and must be cleared when the underlying
  state is reset.


  Apply this standard:

  1) Use safe, stable cache keys

  - Don’t use whole mutable objects (or objects that change every keystroke) as cache
  keys.'
repository: facebook/react#b14
label: Caching
language: TSX
comments_count: 2
repository_stars: 251893
---

Caches must not grow without limit and must be cleared when the underlying state is reset.

Apply this standard:
1) Use safe, stable cache keys
- Don’t use whole mutable objects (or objects that change every keystroke) as cache keys.
- Prefer primitive/stable identifiers (e.g., `sourceVersion`, content hash, or a compact string) derived from the relevant inputs.

2) Bound cache lifetime/size
- Implement LRU (or TTL) so old entries are evicted and promises/results don’t accumulate forever.

3) Invalidate on force reset
- When performing a “force reset,” clear all state that affects derived computations and also drop any cached/derived results tied to prior state (e.g., don’t preserve flags like `showInternals`).

Example pattern (LRU + safe key + reset clearing):

```ts
// Pseudocode: replace with your preferred LRU/TTL implementation
const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({
  max: 200,
  ttlMs: 30_000,
});

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = JSON.stringify({
    // use only the inputs that affect output
    source: store.source,
    showInternals: store.showInternals,
    // or a hash/version instead of full text
  });

  let cached = tabifyCache.get(key);
  if (!cached) {
    cached = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
    tabifyCache.set(key, cached);
  }
  return cached;
}

function forceReset() {
  // clear client state fully
  dispatchStore({ type: 'setStore', payload: { store: defaultStore /* no preserved flags */ } });

  // clear caches derived from the previous state
  tabifyCache.clear();
}
```

Result: bounded memory usage, fewer stale computations, and correct output after resets.