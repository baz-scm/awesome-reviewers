---
title: Bound Caches, Clear On Reset
description: 'Use caching that is (1) bounded and (2) invalidated intentionally.


  - Don’t use whole mutable objects (e.g., a store instance) as cache keys when the
  object can be recreated frequently (like on every keystroke). Compute a stable,
  minimal key from the specific inputs that affect the result.'
repository: facebook/react#b4
label: Caching
language: TSX
comments_count: 2
repository_stars: 251885
---

Use caching that is (1) bounded and (2) invalidated intentionally.

- Don’t use whole mutable objects (e.g., a store instance) as cache keys when the object can be recreated frequently (like on every keystroke). Compute a stable, minimal key from the specific inputs that affect the result.
- Ensure the cache cannot grow forever. Prefer an LRU (bounded size) and/or TTL so old promises/results are evicted.
- When you perform a “force reset” that should fully clear client state, also clear any caches of derived results so future computations reflect the reset state (don’t preserve output-affecting flags unless that’s explicitly intended).

Example (bounded cache + stable key + reset clearing):

```ts
// Minimal inputs only; avoid using full `store` object as the key.
function cacheKey(store: Store, compilerOutput: CompilerOutput) {
  return JSON.stringify({
    source: store.source,
    showInternals: store.showInternals,
    // include whatever else truly affects tabification
    // (avoid including entire objects)
  });
}

const MAX = 50;
const tabifyCache = new Map<string, Promise<Map<string, ReactNode>>>();

function getFromCache(key: string) {
  const v = tabifyCache.get(key);
  if (v) {
    // LRU touch
    tabifyCache.delete(key);
    tabifyCache.set(key, v);
  }
  return v;
}

function setCache(key: string, value: Promise<Map<string, ReactNode>>) {
  if (tabifyCache.has(key)) tabifyCache.delete(key);
  tabifyCache.set(key, value);
  if (tabifyCache.size > MAX) {
    const oldestKey = tabifyCache.keys().next().value;
    tabifyCache.delete(oldestKey);
  }
}

export function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  const key = cacheKey(store, compilerOutput);
  const cached = getFromCache(key);
  if (cached) return cached;

  const result = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
  setCache(key, result);
  return result;
}

// On force reset:
// - clear any cached derived results tied to previous state
// tabifyCache.clear();
```

Apply this pattern anywhere you memoize based on request/state objects: keep keys stable and small, keep caches bounded, and invalidate them when state is reset.