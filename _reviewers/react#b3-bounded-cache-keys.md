---
title: Bounded Cache Keys
description: 'Caches used for derived UI/compute results must be bounded and correctly
  invalidated.


  - **Avoid unbounded growth**: Don’t key caches by large, frequently changing objects
  (e.g., the whole `store` that may change on every keystroke). Prefer **stable, minimal
  identifiers**.'
repository: facebook/react#b3
label: Caching
language: TSX
comments_count: 2
repository_stars: 251883
---

Caches used for derived UI/compute results must be bounded and correctly invalidated.

- **Avoid unbounded growth**: Don’t key caches by large, frequently changing objects (e.g., the whole `store` that may change on every keystroke). Prefer **stable, minimal identifiers**.
- **Use eviction/limits**: Implement **LRU/TTL** (or a bounded map) for cached promises/results so older entries are removed.
- **Invalidate on force reset**: When performing a “force reset” of client state, clear related cached derived data (and don’t carry over internal flags that affect derived output).

Example pattern (bounded LRU + stable key):
```ts
// pseudo-implementation: bounded cache
const tabifyCache = new LRUCache<string, Promise<Map<string, ReactNode>>>({ max: 200 });

function tabifyCached(store: Store, compilerOutput: CompilerOutput) {
  // Build a stable minimal key from primitives that actually affect the output
  const key = JSON.stringify({
    sourceVersion: store.sourceVersion, // or a monotonically increasing counter
    showInternals: store.showInternals,
    outputId: compilerOutput.id,
  });

  let cached = tabifyCache.get(key);
  if (!cached) {
    cached = Promise.resolve(tabify(store.source, compilerOutput, store.showInternals));
    tabifyCache.set(key, cached);
  }
  return cached;
}

// On force reset: clear derived caches/state
function forceReset() {
  tabifyCache.clear();
  dispatchStore({ type: 'setStore', payload: { store: defaultStore } });
}
```