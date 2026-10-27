---
title: Bounded Cache Invalidation
description: 'When caching computed results, ensure the cache is both **bounded**
  and **correctly invalidated**.


  - **Do not use large, mutable objects as cache keys.** Instead, use stable minimal
  identifiers (e.g., primitive IDs, hashes of relevant inputs, or explicit tuples
  of the specific fields that affect the result).'
repository: facebook/react#b10
label: Caching
language: TSX
comments_count: 2
repository_stars: 251894
---

When caching computed results, ensure the cache is both **bounded** and **correctly invalidated**.

- **Do not use large, mutable objects as cache keys.** Instead, use stable minimal identifiers (e.g., primitive IDs, hashes of relevant inputs, or explicit tuples of the specific fields that affect the result).
- **Prevent unbounded growth.** Use an **LRU** (or TTL) cache so entries/promises are evicted instead of accumulating per keystroke.
- **On “force reset”, fully clear derived state.** If a reset is meant to wipe client state, don’t preserve debug/internal flags or other inputs; also invalidate/clear any cache entries that depend on the prior state.

Example (bounded, stable-key caching):
```ts
// Pseudocode for an LRU/TTL cache
const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({ max: 50 });

function cacheKey(store: Store, output: CompilerOutput) {
  // Include only fields that affect tabify output
  return JSON.stringify({
    sourceVersion: store.source.version, // or a hash of store.source
    showInternals: store.showInternals,
    outputVersion: output.version,
  });
}

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = cacheKey(store, compilerOutput);
  const cached = tabifyCache.get(key);
  if (cached) return cached;

  const p = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  tabifyCache.set(key, p);
  return p;
}

// On force reset
function resetPlayground() {
  // fully reset state (including showInternals if that’s part of client state)
  // tabifyCache.clear(); // clear derived cached computations if they depend on previous state
}
```